---
library_name: peft
license: apache-2.0
base_model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
tags:
- generated_from_trainer
datasets:
- /workspace/data/postman_finetune_dataset.json
model-index:
- name: outputs/tinyllama-out
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

[<img src="https://raw.githubusercontent.com/axolotl-ai-cloud/axolotl/main/image/axolotl-badge-web.png" alt="Built with Axolotl" width="200" height="32"/>](https://github.com/axolotl-ai-cloud/axolotl)
<details><summary>See axolotl config</summary>

axolotl version: `0.11.0.dev0`
```yaml
base_model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
model_type: AutoModelForCausalLM
tokenizer_type: AutoTokenizer

load_in_4bit: true
load_in_8bit: false

datasets:
  - path: /workspace/data/postman_finetune_dataset.json
    type: alpaca
    field_messages: conversations
    message_property_mappings:
      role: from
      content: value

val_set_size: 0.0
output_dir: ./outputs/tinyllama-out

adapter: qlora
lora_r: 32
lora_alpha: 16
lora_dropout: 0.05
lora_target_linear: true

sequence_len: 2048
sample_packing: true
eval_sample_packing: false
pad_to_sequence_len: true

gradient_checkpointing: true
gradient_checkpointing_kwargs:
  use_reentrant: false
gradient_accumulation_steps: 4
micro_batch_size: 1
num_epochs: 6

optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 0.0002
weight_decay: 0.0
warmup_ratio: 0.1

bf16: auto
tf32: true
flash_attention: true

logging_steps: 1
saves_per_epoch: 1

```

</details><br>

# outputs/tinyllama-out

This model is a fine-tuned version of [TinyLlama/TinyLlama-1.1B-Chat-v1.0](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) on the /workspace/data/postman_finetune_dataset.json dataset.

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 0.0002
- train_batch_size: 1
- eval_batch_size: 1
- seed: 42
- gradient_accumulation_steps: 4
- total_train_batch_size: 4
- optimizer: Use OptimizerNames.ADAMW_BNB with betas=(0.9,0.999) and epsilon=1e-08 and optimizer_args=No additional optimizer arguments
- lr_scheduler_type: cosine
- lr_scheduler_warmup_steps: 9
- training_steps: 90

### Training results



### Framework versions

- PEFT 0.15.2
- Transformers 4.52.4
- Pytorch 2.6.0+cu124
- Datasets 3.6.0
- Tokenizers 0.21.1