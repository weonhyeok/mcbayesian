# Bayesian A/B 테스팅 (Monte Carlo 예제)

이 저장소는 **이진 전환율 데이터**(binary outcome)를 대상으로 한  
**Bayesian A/B 테스트 최소 예제**입니다.

특징:
- **2025년 08월 데이터**를 경험적 사전분포(prior)로 사용
- **2025년 09월 A/B 실험 데이터**를 우도(likelihood)로 사용
- Beta–Binomial 모델 기반 Monte Carlo 시뮬레이션
- 데이터 생성과 분석을 **CSV 파일 기준으로 완전히 분리**

---

## 프로젝트 구조

```bash
mcbayesian/
│
├── 1_createData.py # 데이터 생성 및 CSV 저장
├── 2_analyze.py # CSV 불러와 Bayesian 분석
├── conversion_data_2025_08_09.csv
└── README.md
```

---

## 1단계. 데이터 생성 (1_createData.py)

### 데이터 구성

- **2025-08**
  - 베이스라인 전환율 데이터
  - 표본 수: 1,000

- **2025-09**
  - A/B 실험
  - A 그룹: 500
  - B 그룹: 500

- Outcome
  - 전환 여부 (0/1)

### 실행

python 1_createData.py

#### 실행 결과

```yaml
Saved file: conversion_data_2025_08_09.csv

                  count  sum   mean
month   group
2025-08 baseline   1000   95  0.095
2025-09 A           500   53  0.106
        B           500   59  0.118
```

```yaml
month   group       y
2025-08 baseline    0
2025-08 baseline    1
...
2025-09 A           0
2025-09 B           1
```

### 2단계. Bayesian 분석 (2_analyze.py)
#### 분석 개요
- 우도(Likelihood)
    - 전환 여부에 대한 Bernoulli 분포
- 사전분포(Prior)
    - 2025년 08월 데이터를 기반으로 한 Beta 분포
    - prior strength = 200 (가상 표본 수)
- 사후분포(Posterior)
    - 2025년 09월 A/B 실험 데이터를 반영하여 업데이트

#### 실행

python 2_analyze.py

#### 실행 결과

```yaml

aug_empirical_rate: 0.095
prior_beta: (20.0, 182.0)
sep_counts: {'A': {'success': 53, 'n': 500}, 'B': {'success': 59, 'n': 500}}

posterior_mean_A: 0.10396026966369441
posterior_mean_B: 0.11251221071471183

P(B > A | data): 0.69829
uplift_mean: 0.00855194105101742
uplift_95_CI: (-0.0238, 0.0411)

```

#### 결과 해석
- 2025년 08월 평균 전환율: 9.5%
- 사후 평균 전환율:
    - A 그룹: 10.4%
    - B 그룹: 11.3%
- B가 A보다 전환율이 높을 확률:
    - 약 70%
- 전환율 차이에 대한 95% 신뢰구간(credible interval):
    - 0을 포함 → 효과의 불확실성 존재

- 결론:
    - B가 더 나을 가능성은 있으나
    - 정책 또는 서비스 전면 도입을 결정하기에는 아직 근거가 충분하지 않음

### 핵심 요약
- 8월 데이터는 기존 정보(prior)로 사용
- 9월 A/B 실험은 새로운 증거(likelihood)
- Bayesian A/B 테스트는 이 둘을 일관된 확률 체계로 결합
- 결과는 “유의성”이 아닌 “확률”로 해석 가능

### 확장 가능 주제
- prior strength에 대한 민감도 분석
- Bayesian 실험 중단(stopping rule)
- 동일 데이터에 대한 Frequentist A/B 테스트 비교
- 계층적(hierarchical) 사전분포 확장

### 한 줄 요약
- Bayesian A/B 테스트는 과거 데이터와 현재 실험 결과를 결합하여
- 처치 효과와 의사결정의 불확실성을 직접적으로 정량화하는 방법이다.
