CUDA_VISIBLE_DEVICES=3 \
nohup python -u src/train_bash.py  \
--stage sft  \
--do_predict  \
--dataset CCKS_test \
--finetuning_type lora  \
--checkpoint_dir checkpoint_CCKS_ChatGLMv2_lora_epoch50_1e-4 \
--output_dir evaluation_CCKS_ChatGLMv2_lora_epoch50_1e-4 \
--per_device_eval_batch_size 8   \
--predict_with_generate \
--use_v2 >> pred_CCKS_ChatGLMv2_lora_epoch50_1e-4.txt 2>&1 &