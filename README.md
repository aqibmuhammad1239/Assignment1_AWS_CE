# Assignment1_AWS_CE
# UniEvent: Scalable University Event Management System

## Phase 1: API Selection & Logic
As a Cloud Architect, I have chosen to integrate the **Ticketmaster Discovery API** for this project.

### API Justification
* **Data Structure**: It provides structured JSON including title, date, venue, and image URLs.
* **Automation**: It allows the system to fetch real-time event data automatically rather than using manual entry.

### Local Verification
I verified the API functionality using a Python script (`fetch_events.py`) which successfully retrieves event details.
## Phase 2: Network Infrastructure (VPC)
[cite_start]As the Cloud Architect, I designed a custom VPC to host the UniEvent platform securely and reliably[cite: 15].

### Architectural Design
* [cite_start]**Multi-AZ Deployment**: The network is spread across two Availability Zones (AZs) to ensure the system is fault-tolerant and remains available even if one data center fails.
* **Public Subnets**: Two public subnets were created to house the Application Load Balancer and NAT Gateways.
* [cite_start]**Private Subnets**: Following security best practices, the web application runs on multiple EC2 instances inside private subnets, protecting them from direct internet access[cite: 16, 18].
* [cite_start]**Connectivity**: A Regional NAT Gateway was configured so the private instances can securely fetch data from the Ticketmaster API[cite: 9, 19].
* [cite_start]**S3 Gateway Endpoint**: I implemented an S3 Gateway endpoint to allow private, secure media uploads to S3 without traversing the public internet[cite: 16, 21].

### VPC Resource Map
![VPC Resource Map](images/VPC_Resource_Map.png)
