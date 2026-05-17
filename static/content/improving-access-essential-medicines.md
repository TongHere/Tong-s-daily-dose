# Improving Access to Essential Medicines via Decision-Aware Machine Learning

**Date:** May 17, 2026

**Paper:** Chung, A. T.-H. *et al.* [Improving access to essential medicines via decision-aware machine learning](https://www.nature.com/articles/d41586-026-01152-0). *Nature* (2026).

**Author:** [Angel Tsai-Hsuan Chung](https://angel-chung.github.io/fieldwork/)

---

Key takeaway : 

Medicine distrubution problem in Sierra Leone. 

1. Sierra Leone's medical supply chain faces significant challenges, including inaccurate demand forecasting driven by manual Excel-based data management. Operational and supply chain workflows are frequently misaligned, while a lack of technical expertise and weak logistics infrastructure hamper the management of complex distribution networks.
2. The framework utilizes innovative framework to solve the probems. Mutitasking leanring, catacylic piror and decision aware learning.
  - First : Forcasting demain based on the medicine, and facilities. in this way, it can help with the knowledge transfer from rich data location to poor data location
  - Using catacylic piror to solve the issues of systematic data shortage such as the staff shortage and incoporated the population based model. 
  - Using decsion aware learning to make model focus on the demand and prioritize predictions that matter most to the actual allocation choice.

-- 

Reading note - From the Article : 

1. Misalignment between operational systems and supply chain operations, insufficient technical expertise, and lack of infrastructure to manage complex supply chains.
2. Program initiatives by Health Care Initiative(FHCI) as one of its largest healthcare. Provide the product in Sierra leona - for pregnate woman and the children.
3. The medicines are distributed to healthercare facilities only once a quater which can lead to substantial shortages in one location even there are adequate spply in other location.
4. The method of design more adaptive supply chains have fail because of the logistical challenges.
5. The forecasting demand is difficult because of its jigh variability, die to demand shocks caused by natural disasters or disease outbreak and periodic trends casuesd by seasonal disearse such as malaria.
6. Existing strategies utilized in global health contexts including replying on historical cinsumption data, morbidity-based forecasting or proxy estimates. Futhermore, lack of modern computing infrasturcture, decision-makers in pratice rely primarily on ad hoc manual foractsing or on excel spreadsheet with high forcasting errors.
7. The framework introduce - Noval machine learning framework 1. it makes effective use of limited and noisy historical data, and it is scalable and can be deployed in limited computed environment.  The system leverages machine learning to predict demand on the basis of features constructed from historical data, and then applies stochastic optimization to compute the bast allocation on the basis of this model's perdiction.
8. For tackle data scarcity and quality challenges. The system uses a multi-task learning strategy to share daa across different healthcare facilities along with a novel descision-aware learning algorithm that aligns the prediciton loss with the downstream allocation objective. It also use catalytic priors with auxilary data sources to mitigate data inequity.
9. Catalytic priors are a Bayesian technique used to stabilize high-dimensional, complex "working models" by shrinking them toward simpler models. They work by augmenting observed data with synthetic data generated from a simpler, more stable model, effectively acting as an informative prior that aids estimation when sample sizes are small.
10. The system helps 2 million women and childran under 5 years of age. The gains were extremely cost-effective, requiring only US 30 monthly serveer fee and no addtional workforce.
11. Figure1 illustrates the system that we developed and deployed. Unlike the earlier two-level approach, our system directly generates facility-level allocations, which are provided to district pharmacists to support their decision-making. Our system begins by pulling monthly consumption data from DHIS2, along with quarterly data on total cen-tral stock available for allocation and corresponding expiry dates from the mSupply warehouse management system (details inMethods). It then performs substantial preprocessing to ensure data reliability and construct informative features for prediction (details in Supplementary Information1.2).
12. Our prediction and optimization algorithm (Fig.1, box) can be divided into two components. First, we predict the demand distri-bution for each facility–product pair using a novel decision-aware machine learning framework (described below). Second, given the demand forecasts, our optimization algorithm outputs allocation decisions directly from the central stock to individual health facilities, which are designed to minimize the expected shortage of medicines. In particular, for each product, it aims to minimize unmet demand—the total number of units of requested product that go unfulfilled—across facilities. To account for the stochastic nature of demand, we use the expected unmet demand according to probabilistic demand forecasts. This optimization problem can be solved efficiently via linear program-ming using a sample average approximation48. Once the allocation is determined, our system assigns each batch of supplies to a warehouse on the basis of proximity, central stock availability and product expi-ration dates (Methods).

---

## Explanation from Gemini

Here is the compiled list of all the text segments, mathematical formulations, and notes you have provided in our session so far, organized by topic for easy access:

---

### 1. Context & Problem Overview

**Original Text:**

> "In this context, a low-cost and promising avenue to scalably reduce shortages is to better match limited supply with patient demand using a combination of prediction and optimization [24–26]. In particular, given accurate facility-level demand forecasts for a product, existing supply chain optimization techniques [27–29] optimize facility-level allocations to minimize unmet patient demand."

**Key Takeaways:**

- **Goal:** Scalably reduce medical resource shortages at the health facility level.
- **Strategy:** Combine machine learning (prediction) with mathematical programming (optimization).
- **Objective:** Minimize unmet patient demand based on facility-level forecasts.

---

### 2. The Operational Challenges in Sierra Leone

**Contextual Summary:**

- **Data Issues:** Forecasting is highly inaccurate because historical data is primarily stored and managed manually in Excel files, leading to fragmentation, data scarcity, and high noise levels.
- **Structural Disconnect:** Operational workflows and supply chain management are completely misaligned with one another.
- **Systemic Bottlenecks:** There is an acute lack of local technical expertise and inadequate infrastructure to support or manage complex, large-scale supply chain logistics.

---

### 3. Machine Learning Framework for Demand Forecasting

**Original Text Insights:**
Traditional methods like ARIMA fail due to extreme data scarcity (e.g., at most 37 monthly observations per facility–product pair from Jan 2020 to Jan 2023). To overcome this, the proposed machine learning framework utilizes three pillars:

#### A. Multi-Task Learning

- **Concept:** Trains a single model across multiple interrelated tasks (all facility–product pairs) to share data and transfer knowledge from data-rich locations to data-poor locations.
- **Grouping:** Splitting products into two main categories: (1) Medicines, and (2) Medical supplies and equipment.
- **Maximum Likelihood Problem Formulation (Separate Estimation Baseline):**

$$ \tilde{\ell}(\mu_n, \sigma_n) = \sum_{n=1}^N \sum_{t=1}^T -\log \mathcal{N}(\xi^*_{t,n} ; \mu_n, \sigma_n^2) $$

- **Feature Engineering (Covariates $x_{t,n}$):** Lagged consumption, product, facility ID/type, geographic coordinates (latitude/longitude), district, facility average consumption over the past 1–6 months, standard deviation over the past 3 and 6 months, sample size, year, month, and global cross-facility average consumption over the past 1–10 months.
- **Model Integration:** A Random Forest is trained on the pooled dataset to predict the mean demand ($\mu_\theta(x)$), assuming variance is constant, and then fitting the standard deviation ($\sigma_\theta(x)$) purely using historical local facility data.

#### B. Catalytic Priors & Mitigating Data Inequity

- **Concept:** Poorer facilities often suffer from severe data inequity (non-randomly missing data or censoring due to staffing shortages), leading to covariate shift and noisy forecasts.
- **Solution:** Introduce a simple, low-bias, population-based model as a Bayesian "catalytic prior" to regularize the machine learning model's predictions in data-poor areas.
- **Population Model:** $\mu_{C,tn} = p_n \cdot r \cdot C$, where $p_n$ is the catchment population, $r$ is the census-derived proportion of women/children (at-risk population), and $C$ is a product-specific demand parameter.
- **Catchment Population ($p_n$) Estimation Pipeline:**

1. Collect health facility coordinates via Google Maps and GRID3.
2. Compute Normalized Difference Vegetation Index (NDVI) via Google Earth Engine to act as a proxy for human activity: $\text{NDVI} = \frac{\text{NIR} - \text{red}}{\text{NIR} + \text{red}}$.
3. Map travel times using Google Earth friction surface data to define catchment areas based on minimal travel time.
4. Extract population counts from WorldPop $100\text{ m} \times 100\text{ m}$ grid cells.

#### C. Decision-Aware Learning

- **Concept:** Traditional models minimize standard prediction errors (like MSE) but are "decision-blind" to downstream optimization consequences. Decision-aware learning alters the training algorithm to prioritize predictions that matter most to the actual allocation choice.
- **Mathematical Objective (Taylor Expansion Approach):**
Approximating the complex downstream decision loss via a first-order Taylor expansion around the true demand vector, resulting in a **weighted absolute error loss**:

$$ \hat{\theta} = \arg\min_{\theta} \sum_{n=1}^N \sum_{t=1}^T |w_{t,n} \cdot (\mu_\theta(x_{t,n}) - \xi^*_{t,n})| $$

- **Analytic Weights via KKT Conditions:**
By solving the Lagrangian of the allocation problem and applying Karush-Kuhn-Tucker (KKT) conditions, the operational weights simplify to:

$$ w_{t,n} \approx \mathbb{P}[\Xi_{tn} > a_{tn}^*(\mu^*) + s_{tn}] + c $$

*Insight:* This mathematically upweights training examples for health facilities that are highly likely to face unmet demand (stockouts).

---

### 4. Stochastic Optimization Model

**Concept:**
An optimization algorithm designed to distribute a fixed, central medical stockpile to individual health facilities while minimizing the expected total unmet demand across the network.

#### Variables & Parameters:

- $N \in \mathbb{N}$: Total number of facilities.
- $b \in \mathbb{R}$: Fixed total available central stock ("budget").
- $a_n \in \mathbb{R}^N$: Allocation decision intended for facility $n$.
- $s_n \in \mathbb{R}^N$: Existing stock on hand at facility $n$.
- $\Xi_n \sim P_\Xi$: Random variable representing future demand at facility $n$.

#### Formulation:

$$\begin{aligned} \min_{a \in \mathbb{R}^N} \quad & \sum_{n=1}^N \mathbb{E}*{\Xi_n \sim P*\Xi} \left[ \max(0, \Xi_n - a_n - s_n) \right]  \text{subject to} \quad & \sum_{n=1}^N a_n \le b,  & a_n \ge 0, \quad \forall n \in 1, \dots, N \end{aligned}$$

---

### 5. Impact Evaluation Methodology: Synthetic Difference-in-Differences (SynthDiD)

**Concept:**
Because only a small number of districts received the system intervention, SynthDiD is used to establish robust causal inference by balancing pre-treatment patterns between treated and control groups without relying on rigid parallel trend assumptions.

#### Mechanics:

- **Unit Weights ($\hat{\omega}_n^{\text{sdid}}$):** Aligns the baseline *levels* of control facilities to match the treated group before intervention.
- **Time Weights ($\hat{\lambda}_t^{\text{sdid}}$):** Aligns pre-treatment *trends* with post-treatment periods to isolate time-based shocks.

#### Core Estimator (ATT):

$$ (\hat{\tau}, \hat{\mu}, \hat{\alpha}, \hat{\beta}) = \arg\min_{\tau, \mu, \alpha, \beta} \sum_{n=1}^N \sum_{t=1}^T \left( Y_{nt} - \mu - \alpha_n - \beta_t - \tau W_{nt} \right)^2 \hat{\omega}_n^{\text{sdid}} \hat{\lambda}_t^{\text{sdid}} $$

- $Y_{nt}$: Average consumption for facility $n$ at time $t$.
- $\alpha_n, \beta_t$: Facility and time fixed effects.
- $W_{nt}$: Binary treatment assignment indicator; $\tau$: The estimated treatment effect.

#### Event Study Integration:

Compares the treated-to-synthetic-control difference across time against an optimized, multi-period baseline:

$$ (Y_{t}^{\text{Tr}} - Y_{t}^{\text{Co}}) - (Y_{\text{baseline}}^{\text{Tr}} - Y_{\text{baseline}}^{\text{Co}}) $$

Where the baseline means are dynamic products of the optimized pre-treatment time weights:

$$ Y_{\text{baseline}}^{\text{Tr}} = \sum_{t=1}^{T_{\text{pre}}} \hat{\lambda}*t^{\text{sdid}} Y*{t}^{\text{Tr}} \quad \text{and} \quad Y_{\text{baseline}}^{\text{Co}} = \sum_{t=1}^{T_{\text{pre}}} \hat{\lambda}*t^{\text{sdid}} Y*{t}^{\text{Co}} $$