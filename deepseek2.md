# Notes for DeepSeek Paper

**Title:** _DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning_

---

## 1. Overview

### 1.1. DeepSeek-R1-Zero and DeepSeek-R1

- **DeepSeek-R1-Zero**: A model trained **without** supervised fine-tuning, but **with** reinforcement learning (RL).
- **DeepSeek-R1**: A variant distilled from Qwen and Llama, incorporating supervised fine-tuning (SFT) data **before** RL.

**Key Points:**

- Previous approaches suffered from:
  - Poor readability
  - Mixing languages
- The DeepSeek approach uses multi-stage training and “cold-start” data **before** RL.
- Performance is comparable to _OpenAI-o1-1217_ on reasoning tasks.
- Post-training (RL) is crucial for improved accuracy on reasoning tasks, alignment with social values, and adaptation to user preferences—requiring fewer computation resources compared to full retraining.
- Effective test-time scaling remains an open question for the research community.

### 1.2. Major Components

1. **Process-based Reward Model**
2. **Reinforcement Learning**
3. **Search Algorithms**

---

## 2. Goal of the Paper

1. To explore how large language models (LLMs) can develop **reasoning capabilities** without any supervised data, focusing on a purely RL-driven, self-evolution process.
2. To use **DeepSeek V3 Base** as the starting model and employ **GRPO** (Group Relative Policy Optimization) as the RL framework, thereby improving performance on reasoning tasks.

---

## 3. DeepSeek-R1 Zero

- **DeepSeek-R1 Zero** applies RL **directly** to the DeepSeek V3-Base model, initially without supervised fine-tuning (SFT).
- After RL converges, new SFT data is created (via rejection sampling on the RL checkpoint) and combined with supervised data from DeepSeek-V3 in domains such as writing and QA.
- The DeepSeek V3-Base Model is then re-trained (fine-tuned) on this expanded dataset, followed by **another** RL step that includes prompts from all scenarios.
- The final result is **DeepSeek-R1**, distilled from Qwen and Llama.

### 3.1. Contributions

- **Post-Training with RL**: Directly applying RL to a base model without initial SFT.
- **Enhanced Chain of Thought**: Encourages exploration and production of detailed reasoning steps.
- **Self-Verification & Reflection**: DeepSeek-R1 Zero demonstrates self-verification, reflection, and generating advanced CoTs—an important milestone for the research community.
- **Two RL Stages**:
  1. Discover improved reasoning patterns.
  2. Align with human preferences.
- **Two SFT Stages**: Provide seeds for both reasoning and non-reasoning capabilities.

### 3.2. Distillation

- Smaller, distilled models (from larger Qwen or Llama) perform surprisingly well.
- Fine-tuned dense models outperform certain benchmarks.

---

## 4. Evaluation Results

| Aspect             | Performance                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------- |
| **Reasoning Task** | DeepSeek-R1 achieves **79.8**, slightly surpassing OpenAI-o1-1217. Better than DeepSeek V3. |
| **Knowledge**      | DeepSeek-R1 outperforms other closed-source models in various knowledge tests.              |

---

## 5. Approach Summary

1. **Large-Scale Reinforcement Learning**: Applied directly on top of a base LLM.
2. **DeepSeek-R1 Zero**: Base model + RL **without** any SFT data.
3. **DeepSeek-R1**: RL starting from a checkpoint already fine-tuned with thousands of long chain-of-thought examples.
4. **Distillation**: Reasoning ability is further distilled into smaller dense models from the main RL-trained checkpoint.

### 5.1. DeepSeek-R1-Zero: RL on the Base Model

- Minimizes reliance on SFT data by gathering data **from** RL.
- Emphasizes the potential of LLMs to develop reasoning abilities autonomously via self-evolution.

#### 5.1.1. Reinforcement Learning Algorithm

- **Group Relative Policy Optimization (GRPO)**

#### 5.1.2. Prompting Format

A conversation between User and Assistant. The user asks a question, and the Assistant solves it.
The assistant first thinks about the reasoning process in its mind and then provides the user
with the answer. The reasoning process and answer are enclosed within <think> </think> and
<answer> </answer> tags, respectively.

User: [prompt here]
Assistant:
<think> [reasoning process here] </think>
<answer> [answer here] </answer>

#### 5.1.3. Reward Model

- **Accuracy Reward**
- **Formatting Rewards** (adhering to `<think>` & `<answer>` tags)

#### 5.1.4. Training Template

- Guides the base model to follow specified instructions.
- _“Aha moment”_: An intermediate version of DeepSeek-R1-Zero learned to generate more structured outputs with reflection and verification.

### 5.2. DeepSeek-R1

- Begins with a **small** SFT dataset (long chain-of-thought examples).
- Uses few-shot prompting, self-generated CoT outputs (from DeepSeek-R1-Zero), and human annotation.
- Retrains the base model, and finishes with an **additional** RL process considering all prompt scenarios.

---

## 6. News & Miscellaneous

### 6.1. Founder

- **Name**: Wun Fung-Laing
- **Background**: Graduated from Zhejiang University (Electrical Engineering) and holds a master’s in Communication Engineering.
- **Affiliation**: High Flyer (Hangzhou-based hedge fund and AI company founded in 2015).

### 6.2. GPU Fight

- Aim: Not to reduce chips but to make them more efficient.
- American ban on advanced chips to China; rumor of ~50k GPUs in use.
- **Jevons Paradox**: Increasing efficiency often leads to higher overall consumption.

### 6.3. Privacy

- **Information Collected**:
  - Device model, OS, keystroke patterns, IP address, system language
  - Data from login, sign-up, or linked services
  - Shared with service providers, business partners, corporate groups, and for legal obligations
- **User Rights**:
  - Know how personal data is collected and used
  - Access, change, oppose, or withdraw consent
  - Request a copy or deletion of data
- **Data Storage**:
  - Collected and stored in China
  - Retention depends on data type

### 6.4. Political Speech

- Filtered by default.
- One-China Policy is the default stance.

### 6.5. Cost

- Estimated at **\$6M** (excludes smaller runs, data generation, and DeepSeek R1 training transactions).

### 6.6. Memory

- **16 × 80 GB** GPU memory in use.

### 6.7. “Unsensor” Version

- An uncensored variant might exist in Perplexity (unverified rumor).

---

_End of DeepSeek Paper Notes_
