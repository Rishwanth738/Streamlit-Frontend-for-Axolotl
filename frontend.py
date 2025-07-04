import streamlit as st
import os
import subprocess
import time
from pathlib import Path
import threading
import requests
from dotenv import load_dotenv

yaml_dir = Path("examples")
outputs_dir = Path("outputs")
container_name = "axo-ui"
st.set_page_config(layout="wide")
st.title("Axolotl Fine-Tuning UI")


st.header("1. Fine-tuning Configuration")
yaml_files = list(yaml_dir.rglob("*.yaml"))

if not yaml_files:
    st.warning("No YAML files found in examples/ directory.")
else:
    selected_yaml = st.selectbox("Select YAML config file", yaml_files)
    with open(selected_yaml, "r") as f:
        yaml_content = f.read()

    edited_yaml = st.text_area("Edit YAML (optional)", yaml_content, height=400, key="yaml_editor")

    if st.button("Run Fine-tuning"):
        with open(selected_yaml, "w") as f:
            f.write(edited_yaml)

        st.session_state["finetune_log"] = ""
        st.session_state["running"] = True
        
        result = subprocess.run(
            ["docker", "ps", "-a", "-q", "-f", f"name={container_name}"],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            subprocess.run(["docker", "rm", "-f", container_name])

        subprocess.run([
            "docker", "run", "--gpus", "all", "-dit",
            "--name", container_name,
            "-v", "F:\\Axolotl:/workspace/axolotl",
            "-v", "F:\\Axolotl\\data:/workspace/data",
            "-v", "F:\\Axolotl\\outputs:/workspace/outputs",
            "axolotlai/axolotl:main-latest"
        ])

        yaml_path_in_container = f"/workspace/axolotl/{selected_yaml}".replace("\\", "/")
        command = [
            "docker", "exec", "-i", container_name,
            "python3", "-m", "axolotl.cli.train", yaml_path_in_container
        ]
        command_str = " ".join(command)
        st.session_state["finetune_log"] += f"$ {command_str}\n"

        st.success(f"Fine-tuning started with {selected_yaml.name}")
        st.session_state["process"] = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

st.header("2. Terminal Logs")
if st.session_state.get("running") and "process" in st.session_state:
    proc = st.session_state["process"]
    log_placeholder = st.empty()
    logs = st.session_state.get("finetune_log", "")

    if st.button("Refresh Logs"):
        while proc.poll() is None:
            line = proc.stdout.readline()
            if line:
                logs += line
                log_placeholder.text_area("Logs", logs, height=400)
                st.session_state["finetune_log"] = logs
            else:
                break

    if proc.poll() is not None:
        logs += proc.stdout.read()  # Flush remaining output
        st.session_state["running"] = False
        st.session_state["finetune_log"] = logs
        st.success("Fine-tuning completed")
        log_placeholder.text_area("Logs", logs, height=400)


# 3. Inference
st.header("3. Inference")

model_dirs = [d for d in outputs_dir.glob("*") if d.is_dir()]
if model_dirs:
    selected_model = st.selectbox("Select fine-tuned model", model_dirs)
    prompt_input = st.text_area("Prompt input", height=200)

    max_tokens = st.slider("Max tokens", min_value=32, max_value=4096, value=1024, step=32)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
    top_p = st.slider("Top-p", min_value=0.0, max_value=1.0, value=0.95, step=0.01)

    if st.button("Run Inference"):
        ckpt_path_in_container = f"/workspace/axolotl/{selected_model}".replace("\\", "/")
        cmd = [
            "docker", "exec", "-i", container_name,
            "python3", "/workspace/axolotl/run_infer.py",
            "--prompt", prompt_input,
            "--ckpt", ckpt_path_in_container,
            "--max_tokens", str(max_tokens),
            "--temperature", str(temperature),
            "--top_p", str(top_p)
        ]
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            st.text_area("Model Output", result, height=300)
        except subprocess.CalledProcessError as e:
            st.error("Error during inference:")
            st.text_area("Traceback", e.output, height=300)
else:
    st.warning("No models found in outputs/ directory.")

def validate_js(code1,code2):
            input_str = code1 + '<<SPLIT>>' + code2
            result = subprocess.run(
            ["node", "validate.js"],
            input=input_str,
            capture_output=True,
            text=True)

            if result.returncode == 0:
                return True
            elif result.returncode == 1:
                return False
            else:
                raise RuntimeError(f"Validator error: {result.stderr}")


load_dotenv()
api_url = os.getenv("AZURE_URL")
if not api_url or not api_url.strip():
    st.error("AZURE_URL is not set in your .env file or is empty. Please check your .env configuration.")
    st.stop()

def validate_scripts(script1, script2):
    prompt = f'''
    <|system|>
    You are an excellent validator who checks for similarity between 2 postman scripts and gives a score based on how similar they are when compared for their logic.
    {script2} is generated by a fine tuned model and {script1} is the expected result.

    <|user|>
    ###Instructions:
    - Grade them out of 100.
    - Give the score based on how similar the 2 codes are when it comes to logic.
    - Reduce marks for tests that are missing from {script2} when compared to {script1}.
    - Reduce marks if the code in {script2} is in the older Postman format that is if it uses tests[...] or postman.set(...) or postman.get(...).
    - **Do not give me any other remarks or comparison between the codes just give me the score**


    ###Output:
    The total similarity score is:
    '''

    payload = {
        "systemprompt": "",
        "userprompt": prompt,
        "max_completion_tokens": 2048,
        "temperature": 0.6,
        "top_p": 0.75,
        "stop": None,
        "model": "gpt-4.1-mini"
    }

    try:
        response = requests.post(api_url, json=payload, timeout=1600)
        response.raise_for_status()
        return response.text.strip().strip('`\n"\' ')
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling validation API: {str(e)}")
        return None


st.header("4. Validation")
model_dirs = [d for d in outputs_dir.glob("*") if d.is_dir()]
if model_dirs:
    selected_model = st.selectbox("Select fine-tuned model", model_dirs, key="validation")
    prompt_input = st.text_area("Prompt input", height=200, key="pi")

    max_tokens = st.slider("Max tokens", min_value=32, max_value=4096, value=1024, step=32, key="si1")
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.05, key="si2")
    top_p = st.slider("Top-p", min_value=0.0, max_value=1.0, value=0.95, step=0.01, key="si3")

    if st.button("Run Validation"):
        ckpt_path = f"/workspace/axolotl/{selected_model}".replace("\\", "/")
        cmd = [
            "docker", "exec", "-i", container_name,
            "python3", "/workspace/axolotl/run_infer.py",
            "--prompt", prompt_input,
            "--ckpt", ckpt_path,
            "--max_tokens", str(max_tokens),
            "--temperature", str(temperature),
            "--top_p", str(top_p)
        ]
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            st.session_state["validation_result"] = result
            st.text_area("Model Output", result, height=300, key="vout")
        except subprocess.CalledProcessError as e:
            st.error("Error during inference:")
            st.text_area("Traceback", e.output, height=300, key="verr")
    
    if "validation_result" in st.session_state:
        eresult = st.text_area("Expected Output", height=300, key="expected_output")
        
        if st.button("Validate Output"):
            if not eresult.strip():
                st.warning("Please enter expected output to validate against")
            else:
                with st.spinner("Validating output..."):
                    gen_output = st.session_state["validation_result"]
                    score = validate_scripts(eresult, gen_output)
                    
                    if score is not None:
                        try:
                            score_value = int(score.split(":")[-1].strip())
                            st.metric("Similarity Score", f"{score_value}/100")
                            
                            if score_value >= 80:
                                st.success("Excellent match!")
                            elif score_value >= 60:
                                st.warning("Moderate match - some differences exist")
                            else:
                                st.error("Poor match - significant differences")
                                
                            st.text_area("Validation Details", score, height=200)
                        except (ValueError, AttributeError):
                            st.text_area("Validation Details", score, height=200)
    else:
        st.warning("Run validation first to generate output before validating.")
else:
    st.warning("No models found in outputs/ directory.")

