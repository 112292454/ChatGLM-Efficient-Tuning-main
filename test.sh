CUDA_VISIBLE_DEVICES=3 \
nohup python -u src/train_bash.py  \
--stage sft  \
--do_predict  \
--dataset WebQSP_test \
--finetuning_type lora  \
--checkpoint_dir checkpoint_WebQSP_ChatGLMv2_lora_epoch100 \
--output_dir evaluation_WebQSP_ChatGLMv2_lora_epoch100 \
--per_device_eval_batch_size 8   \
--predict_with_generate \
--use_v2 >> pred_WebQSP_ChatGLMv2_lora_epoch100.txt 2>&1 &