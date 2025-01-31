This is note for deepseek paper.
DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

1. DeepSeek-R1-Zero and DeepSeek-R1. DeepSeek-R1-Zero

Model train without supervised fine tunning but with reinforment learning.

- With previous approaches, it has challenges like poor readability, and languages mixing.

- Use the approach like multi-stage training and cold start data before RL.

- Achieves performance comparable to OpenAI-o1-1217 on reasoning task.

- DeepSeek R1 is distilled from Qwen and Llama

- post-training (like reinforment learning) has emerged as an important component of the full training pipeline. This will increase the acurracy on reasoing task, align with social value and adapts to user perferences.and require less computation resource.

- effective test-time scaling remains an open-question for the research community.

1.  Process-based reward model
2.  Reinforment learning
3.  Search algorithms

- Goal of paper

1.  Explore LLM to develop reasoning capabilities without any supervised data. Focusing on self-evolution throught a pure RL process.
2.  DeepSeek V3 Base as the base model, and employ GRPO as RL framework to improve modle performance in reasoing.

DeepSeek R1 Zero

- DeepSeekR1 : incorporates a small amount of cold-start data (SFT data) to fine-tune the DeepSeek V3-Base model.
- Follow that, perform the reasoning oriented RL like DeepSeek-R1-Zero
- Upon nearing converagce in RL process, we create new SFT(supervise fine tune) data through rejection sampling on the RL checkpoint, combined with supervised data from deepseek-V3 in domain such as writing, QA.
- Then re-trained the DeepSeek-V3-Base Model
- After fine-tunning with the new data, the checkpoint undergoes an additional RL process, taking into account prompts from all scenarios.
- distilled Qwne and Llama

  1.1 Contributions

- Post Training : Directly using RL to the base model without SFT.
- Approach allow model to explore chain of thought for solving complex problem.
- Deepseek R1 Zero demonstrates capabilities as Self-Verification, reflection and generating CoTs,marketing a significant milestone for the research commnuity.
- Two RL stages - aiming at discovering improved reasoning patterns and aligining with humman preferance.
- Two SFT stages that serves as the seed for models reasoning and non reasoning capabilities.

  1.2 Distillation

- Smaller model distalled from large model perform good.
- Fine-tuned densed model outperform benchmark.

Evaluation Result

- Reasoning task: a. DeepSeek-R1 achieves 79.8, slightly surpassing OpenAI-o1-1217. DeepSeek R1 perform better that DeepSeekV3
- Knowledge : DeepSeek R1 outperform other close source model

Approach :

1. Large Scale reinforment learning.
2. DeepSeek R1 Zero - Applied RL directly to the base model without any SFT data.
3. DeepSeek R1, whichi applied RL starting from a checkpoint fine-tuned with thousands of long Chain of thought Examples.
4. Distill the reasoning capability from DeepSeek-R1 small dense models.

2.2 DeepSeek-R1-Zero: Reinforcement Learning on the Base Model

1. Not use a lot SFT data, but gathering data from RL.
2. explore the potential of LLMs to develop reasoning capabilities without any supervised data,focusing on their self-evolution through a pure reinforcement learning process.
3. Reinforment Learning Algorithm:

- Group Relative Policy Optimization
- Prompt they use :
  """
  A conversation between User and Assistant. The user asks a question, and the Assistant solves it.
  The assistant first thinks about the reasoning process in the mind and then provides the user
  with the answer. The reasoning process and answer are enclosed within <think> </think> and
  <answer> </answer> tags, respectively, i.e., <think> reasoning process here </think>
  <answer> answer here </answer>. User: prompt. Assistant

""" 4. Reward Model:

- Accuracy Reward
- Format Rewards

5. Training Template:

- Template for guiding the base model to adhere to our specified instruction.
- An interesting “aha moment” of an intermediate version of DeepSeek-R1-Zero
  2.3.1
- DeepSeek-R1 we construct and collect a small amount of long CoT data
  to fine-tune the model as the initial RL actor. 1. few-shot prompting with a long CoT. 2. directly prompting
  models to generate detailed answers with reflection and verification, gathering DeepSeek-R1-
  Zero outputs in a readable format. 3. refining the results through post-processing by human
  annotators.
-

News -

1. Founder : Wun Fung- Laing, Grauduated from 浙江大學電機工程系畢業生、通信工程碩士. Funding High Flyer (Hangzhou-based hedge fund and artificial intelligence (AI) company founded in 2015)
1. GPU fight - Not reduce the chips, but make chips more efficient. Amarican ban advance chips to china. Rummor : 50k GPU. Jevons Paradox - increase the efficient, but will increase the consumption, the resource is more attractive, and more people use it,
1. Privacy -
   Information provide. User Input, Information when contact them.
   This information includes your device model, operating system, keystroke patterns or rhythms, IP address, and system languagues.
   Log in, Sign up or Linked Services. Advertising, Measurement, and other Partners.
   Share information to Service provider, Business Partner, Corporate group and Legal Obligation and Rights
   Your Right: Right to know how they collect, use personal information, right to access, withdraw consent, change, oppose, request a copy of your authorization.
   Depends on what kind of data to keep your data.
   Data is colleted and storage in China
1. Politcal Speech - Filier and One China Policy default.
1. Cost : 6m dollor. but exclude ablations, smaller run, data generation and deepseek R1 training. Transaction information.
1. 16x 80 GB Memory
1. Unsensor version in Preplexity
