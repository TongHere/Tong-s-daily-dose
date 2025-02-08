# What is Model Distillation?

Model Distillation means knowledge transfer from a large model (Teacher model) to a smaller model (Student model) using different distillation methods.

![image.png](C:\Users\User\Documents\Tong's\1image.png)

**_Figure 1. The teacher-student framework for knowledge distillation | Source: [Arxiv](https://arxiv.org/abs/2006.05525)_**

## What is the Impact of Model Distillation?

1. Using a smaller model while maintaining the same accuracy.
2. Reducing compute resources and improving the accessibility of AI applications.

## What is the Method of Model Distillation?

### 1. Logits Distillation

- **First**: Calculate teacher and student’s batch logits.
- **Second**: Compute the loss between them (the difference between them).
- **Third**: Return a weighted average between KL Loss and the cross-entropy loss.

![image.png](C:\Users\User\Documents\Tong's\2image.png)

**_Figure 2. Logits distillation | Source:_** [Deep Dive: Model Distillation with DistillKit](https://www.slideshare.net/slideshow/deep-dive-model-distillation-with-distillkit/274619548)

### 2. Hidden State Distillation

- **First**: The student model is narrower, so select the teacher’s layer and add trainable linear layers to resize the student layer output, ensuring the same width (layer selection and layer adaptation).  
  **Example**:
  - Qwen2.5 1.5B: `num_hidden_layers=28`, `hidden_size=1536`
  - Qwen2.5 14B: `num_hidden_layers=48`, `hidden_size=5120`
- **Second**: Compute the loss per layer per batch between the teacher model and the student model.
- **Third**: Return a weighted average between KL Loss and the cross-entropy loss.

![image.png](C:\Users\User\Documents\Tong's\3image.png)

## Which Examples of Model Distillation?

1. BERT to DistilBERT.
2. Llama-3.1 405B instruct to Llama-3.1 70B instruct.
3. Qwen 2.5 32B and Llama-70B to DeepSeek-R1.

## What’s Next for Model Distillation?

1. Energy-efficient AI.
2. On-device AI (Apple Intelligence AFM - Apple Foundation Model).

## References

- [https://arxiv.org/abs/1503.02531](https://arxiv.org/abs/1503.02531)
- [https://www.youtube.com/watch?v=JE7SuP049mQ](https://www.youtube.com/watch?v=JE7SuP049mQ)
- [https://neptune.ai/blog/knowledge-distillation](https://neptune.ai/blog/knowledge-distillation)
- [https://medium.com/@simon3458/intro-knowledge-distillation-cea0e5d6d842](https://medium.com/@simon3458/intro-knowledge-distillation-cea0e5d6d842)
- [https://www.slideshare.net/slideshow/deep-dive-model-distillation-with-distillkit/274619548](https://www.slideshare.net/slideshow/deep-dive-model-distillation-with-distillkit/274619548)
