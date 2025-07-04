import argparse
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

parser = argparse.ArgumentParser()
parser.add_argument("--ckpt", type=str, required=True)
parser.add_argument("--prompt", type=str, required=True)
parser.add_argument("--max_tokens", type=int, default=1024)
parser.add_argument("--temperature", type=float, default=0.7)
parser.add_argument("--top_p", type=float, default=0.95)
args = parser.parse_args()


tokenizer = AutoTokenizer.from_pretrained(args.ckpt, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    args.ckpt,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
    trust_remote_code=True
)
model.eval()


prompt = {
    "instruction": "Convert the following Postman script from the older v2.1 format to the newer v2.2.0 format.",
    "input": args.prompt,
    "output": ""
}

prompt_str = (
    f"### Instruction:\n{prompt['instruction']}\n\n"
    f"### Input:\n{prompt['input']}\n\n"
    f"### Response:\n"
)

inputs = tokenizer(prompt_str, return_tensors="pt").to(model.device)
with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=args.max_tokens,
        do_sample=True,
        temperature=args.temperature,
        top_p=args.top_p,
        eos_token_id=tokenizer.eos_token_id,
    )

decoded_output = tokenizer.decode(output[0], skip_special_tokens=False)
print(decoded_output.split("### Response:")[-1].strip().removesuffix("</s>"))
