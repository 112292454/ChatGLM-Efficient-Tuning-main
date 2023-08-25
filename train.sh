CUDA_VISIBLE_DEVICES=3 \
nohup python -u src/train_bash.py  \
--stage sft  \
--do_train  \
--dataset WebQSP_train  \
--finetuning_type lora \
--output_dir checkpoint_WebQSP_ChatGLMv2_lora_epoch100  \
--per_device_train_batch_size 4  \
--gradient_accumulation_steps 4  \
--lr_scheduler_type cosine  \
--logging_steps 10  \
--save_steps 1000  \
--learning_rate 5e-5  \
--num_train_epochs 100.0 \
--fp16 \
--use_v2 \
>> result_WebQSP_ChatGLMv2_lora_epoch100.txt 2>&1 &
