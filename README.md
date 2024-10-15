# Secure Encrypted Data Aggregation with PHE Proof of Concept
## Table of Contents
- [Project Overview](#project-overview)
- [User story simulation](#user-story-simulation)
- [Technology Stack](#technology-stack)
- [Setup Instruction](#setup-instruction)
- [Future Enchancements](#future-enchancements)

### Project Overview
The Secure Encrypted Data Aggregation POC is a backend simulation designed to demonstrate the feasibility of securely aggregating encrypted financial data using Partically Homomorphic Encryption. The system ensure that sensitive financial data remains confidential while allow an individual to view the results without exposing raw data.

### User story simulation
1. Data Administrator encrypts and uploads encrypted financial data on a central database
2. Data Analyst requests aggregation operations on the encrypted data
3. System backend performs aggregation on encrypted data without decryption it
4. After computations, it sents a request to data adminstrator for approval to decrypt aggregated results
5. Data gets returned back to data analyst after approval

### Technology Stack
- Python 3.8+
  - Flask
  - phe
  - pytest
  - Docker
  - Github Actions
- SQLite

--- 
### Setup Instruction
#### Prerequisites
- Python 3.8+
- Docker
- Git

---
### Future Enchanments
- Exploring Full Homomorphic Encryption for more complex computations
- Frontend Integration with user friendly interface
- Scalable Storage Solutions into robust database like PostgreSQL or cloud storage
- Enchanced Security with clodu based key management services
- Loggin and Monitoring for audit trails and monitoring tools to track system performance

