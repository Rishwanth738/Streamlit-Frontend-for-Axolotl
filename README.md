# 🦙 Axolotl Fine-Tuning UI

A Streamlit-based frontend that lets you fine-tune LLMs with Axolotl, visualize training logs, run inference, and validate model output — all from a sleek and user-friendly interface. No CLI gymnastics needed.

---

## 🚀 Features

### 🛠️ 1. Fine-Tuning Control
- Select and edit your YAML config files directly from the UI
- Launch fine-tuning jobs inside a Docker container with a single click
- Real-time terminal log streaming from the container

### 🧠 2. Inference Engine
- Load your fine-tuned models from the `outputs/` directory
- Input prompt directly in the UI
- Control generation parameters: `max_tokens`, `temperature`, `top_p`
- See complete generated output instantly

### ✅ 3. Output Validation
- Compare model output against expected output using an OpenAI-powered semantic scoring method
- Displays a qualitative similarity judgment between both scripts
- Helps identify hallucinations, structural mismatches, or logical gaps

---

## 📦 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **Backend/Training**: [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl)
- **Inference**: Hugging Face Transformers
- **Validation**: OpenAI GPT model comparison (via API)
- **Container Runtime**: Docker + NVIDIA GPU support

---

## 📁 Folder Structure

Axolotl-Finetuning-UI/
│
├── examples/ # YAML config files for Axolotl
├── outputs/ # Directory containing fine-tuned model folders
├── run_infer.py # Inference script using HuggingFace Transformers
├── frontend.py # Streamlit UI script (main entrypoint)
├── README.md # You're here!

yaml
Copy
Edit

---

## 🧑‍💻 Getting Started

### 1. Clone this repo
```bash
git clone https://github.com/your-username/axolotl-finetuning-ui.git
cd axolotl-finetuning-ui
2. Start the Streamlit UI
bash
Copy
Edit
streamlit run frontend.py
3. Docker Requirement
Make sure Docker is installed and running. The app automatically creates a container named axo-ui and mounts volumes from:

F:/Axolotl → /workspace/axolotl

F:/Axolotl/data → /workspace/data

F:/Axolotl/outputs → /workspace/outputs

Update these in frontend.py if your paths differ.

📜 License
This project is licensed under the Apache 2.0 License.

This tool uses:

Axolotl (Apache 2.0)

OpenAI API for output validation (requires your own API key)

🧠 Notes
This tool does not include model weights or proprietary datasets.

You are responsible for ensuring your fine-tuned models comply with their respective licenses (especially for LLaMA-family models).

Make sure your OpenAI API key is securely managed if validation is enabled.

🧃 Wanna Contribute?
If you're into LLMs, tools, or just cool UI/UX for model training — PRs are welcome. Let’s build the LLM dev tooling scene together.

Made with ❤️ by Rishwanth
