# Secure Encrypted Data Aggregation with PHE Proof of Concept

## Table of Contents

- [Project Overview](#project-overview)
- [User story simulation](#user-story-simulation)
- [Technology Stack](#technology-stack)
- [Setup Instruction](#setup-instruction)
- [Future Enchancements](#future-enchancements)

### Project Overview

The Secure Encrypted Data Aggregation POC is a backend simulation designed to demonstrate the feasibility of securely aggregating encrypted financial data using Partically Homomorphic Encryption. The system ensure that sensitive financial data remains confidential while allow an individual to view the results without exposing raw data.
Implemented with Flask as the framework in order to have a seamless futrue enchancment into a web application

---

### User story simulation

1. Data Administrator encrypts and uploads encrypted financial data on a central database
2. Data Analyst requests aggregation operations on the encrypted data
3. System backend performs aggregation on encrypted data without decryption it
4. After computations, it sents a request to data adminstrator for approval to decrypt aggregated results
5. Data gets returned back to data analyst after approval

---

### Technology Stack

- Python 3.9
  - Flask
  - Pyfhel
  - pytest
  - Docker
  - Github Actions
- SQLite

---

### Libraries

[Pyfhel]([https://github.com/data61/python-paillier](https://github.com/ibarrond/Pyfhel))

---

### Setup Instruction

#### Prerequisites

- Python 3.9
- Docker
- Git
- C/C++ Compiler
- CMake


#### Installation

1. Clone the Repository

```Shell
git clone https://github.com/your_username/secure_data_aggregation_poc.git
cd secure_data_aggregation_poc
```

2. Build Docker Image

```Shell
git clone https://github.com/your_username/secure_data_aggregation_poc.git
cd secure_data_aggregation_poc
```

3. Running Docker Container

```Shell
docker run -d -p 5000:5000 --name secure_data_aggregation_poc secure-data-aggregation-poc
```

---

### Future Enchancements

- Exploring Full Homomorphic Encryption for more complex computations (Including to approximate division with multiplicative inverse techniqu to compute basic financial metrics like profit margins, liquidity ratios or net income)
- Exploring Multiple Homomorphic Encryption Libraries with a comparative analysis
- In Depth Analysis of different t and n values for a more balanced plaintext range with enough security
- Frontend Integration with user friendly interface (with data visulisation techniques)
- Scalable Storage Solutions into robust database like PostgreSQL or cloud storage
- Enchanced Security with clodu based key management services
- Loggin and Monitoring for audit trails and monitoring tools to track system performance
