"""Build LangSmith evaluation dataset from RBI NBFC FAQ.

This module creates a LangSmith dataset with 23 carefully selected questions
from the RBI NBFC FAQ (dated April 23, 2025).
"""

import os
import sys
import argparse
from langsmith import Client
from dotenv import load_dotenv

load_dotenv()

# 23 Key FAQ questions from official RBI NBFC FAQ
RBI_FAQ_SAMPLES = [
    {
        "question": "What is a Non-Banking Financial Company (NBFC)?",
        "answer": "A Non-Banking Financial Company (NBFC) is a company registered under the Companies Act, 1956/2013 engaged in the business of loans and advances, acquisition of shares/stocks/bonds/debentures/securities issued by Government or local authority or other marketable securities. Its principal business is receiving deposits under any scheme or arrangement or any other manner, or lending in any manner. NBFC's financial assets must constitute more than 50% of the total assets and income from financial assets should be more than 50% of the gross income."
    },
    {
        "question": "What are the key differences between banks and NBFCs?",
        "answer": "Key differences: (1) NBFCs cannot accept demand deposits; (2) NBFCs do not form part of the payment and settlement system and cannot issue cheques drawn on itself; (3) Deposit insurance facility of Deposit Insurance and Credit Guarantee Corporation is not available to depositors of NBFCs."
    },
    {
        "question": "Does an NBFC require RBI approval to commence business?",
        "answer": "Yes. Every NBFC is required to obtain a Certificate of Registration (CoR) from RBI to commence/carry on business of a non-banking financial institution as defined in Section 45-I(a) of the RBI Act, 1934."
    },
    {
        "question": "What are the eligibility criteria for registration as NBFC?",
        "answer": "Key criteria include: (1) Minimum Net Owned Fund (NOF) of Rs.2 crore (Rs.10 crore for certain categories); (2) Company should be registered under Companies Act; (3) Should have CRAR of 15%; (4) Should have satisfactory record of at least 10 years in case of companies operating without RBI registration; (5) Board of Directors should have persons with professional and sound credentials."
    },
    {
        "question": "Can NBFCs accept deposits from public?",
        "answer": "Only certain categories of NBFCs can accept deposits subject to specific conditions: (1) Must hold a valid Certificate of Registration with authorization to accept public deposits; (2) Must maintain required investment in approved securities; (3) Must comply with prudential norms on income recognition, asset classification, and provisioning; (4) Must maintain minimum investment grade credit rating; (5) Must comply with deposit mobilization limits based on NOF and credit rating."
    },
    {
        "question": "What is the minimum Net Owned Fund (NOF) requirement for NBFCs?",
        "answer": "The minimum NOF requirement is Rs.2 crore. However, for certain categories like Infrastructure Finance Companies, Core Investment Companies, and Infrastructure Debt Funds, the minimum NOF is Rs.300 crore. For NBFCs-Factors, it is Rs.5 crore, and for Mortgage Guarantee Companies, it is Rs.100 crore."
    },
    {
        "question": "What is the Capital Adequacy Ratio requirement for NBFCs?",
        "answer": "NBFCs are required to maintain a minimum Capital to Risk-weighted Assets Ratio (CRAR) of 15%. This includes a minimum Tier-I capital of 10% of risk-weighted assets. Systemically Important Non-Deposit taking NBFCs (NBFC-ND-SI) and deposit-taking NBFCs must maintain capital adequacy in accordance with the Non-Banking Financial Company - Systemically Important Non-Deposit taking Company and Deposit taking Company (Reserve Bank) Directions, 2016."
    },
    {
        "question": "What are the regulatory reporting requirements for NBFCs?",
        "answer": "NBFCs must submit various regulatory returns including: (1) Annual audited balance sheet and profit & loss account within 3 months of year-end; (2) ALM returns (monthly for deposit-taking NBFCs, quarterly for ND-SI); (3) NBS returns (quarterly for deposit-taking, half-yearly for ND-SI); (4) Certificate from statutory auditors about compliance with prudential norms; (5) CRAR computation; (6) Liquid assets statement; (7) Return on deposits (for deposit-taking NBFCs)."
    },
    {
        "question": "What are the prudential norms for income recognition and asset classification?",
        "answer": "NBFCs must follow RBI's prudential norms: (1) Income recognition on accrual basis only for performing assets; (2) Assets classified as Standard, Sub-Standard (overdue >90 days), Doubtful (overdue >12 months), and Loss assets; (3) Interest on NPAs should not be recognized on accrual basis; (4) Fees/commissions on NPAs recognized on realization basis; (5) Provisioning: 0.25% for standard assets, 10% for unsecured sub-standard, 20-50% for doubtful, 100% for loss assets."
    },
    {
        "question": "What is meant by a Systemically Important NBFC (NBFC-SI)?",
        "answer": "A Systemically Important NBFC is defined as a Non-Deposit taking NBFC with asset size of Rs.500 crore and above. Such NBFCs are subjected to stricter regulatory requirements including maintenance of CRAR, submission of ALM returns, credit concentration norms, and other prudential regulations similar to deposit-taking NBFCs due to their systemic importance to the financial sector."
    },
    {
        "question": "What are the investment and credit concentration norms for NBFCs?",
        "answer": "NBFCs must comply with: (1) Credit exposure to any single borrower should not exceed 25% of owned fund; (2) Credit exposure to single group of borrowers should not exceed 40% of owned fund; (3) Investments in shares of another company should not exceed 25% of owned fund for individual company and 40% for group of companies; (4) These limits can be exceeded by 5% for project financing with board approval."
    },
    {
        "question": "What is the Asset Liability Management framework for NBFCs?",
        "answer": "NBFCs-D and NBFC-ND-SI must have a robust ALM system including: (1) Board-approved ALM policy; (2) ALM Committee meeting at least quarterly; (3) Maturity bucketing of assets and liabilities; (4) Monitoring structural and dynamic liquidity; (5) Negative gap in 1-30 days bucket not to exceed 15% of outflows; (6) Submission of ALM returns (monthly for NBFC-D, quarterly for NBFC-ND-SI); (7) Maintenance of liquidity cushion through liquid assets."
    },
    {
        "question": "What are the Fair Practices Code requirements for NBFCs?",
        "answer": "NBFCs must adopt a Fair Practices Code covering: (1) Disclosure of terms and conditions, all-in-cost, grievance redressal mechanism; (2) General principles on adequate notice for changes in interest rates; (3) Time schedule for processing applications; (4) Non-discriminatory practices; (5) Privacy of customer information; (6) Details of Grievance Redressal Officer; (7) Collection practices to be fair and not involve harassment; (8) Security repossession procedures. The code must be displayed on website and made available to customers."
    },
    {
        "question": "What are the KYC/AML requirements for NBFCs?",
        "answer": "NBFCs must comply with KYC/AML guidelines: (1) Customer identification and verification; (2) Risk-based approach for customer due diligence; (3) PEP identification and enhanced due diligence; (4) Beneficial ownership identification; (5) Maintenance of records for 5 years after business relationship; (6) Reporting of suspicious transactions to FIU-IND within 7 days; (7) Appointment of Principal Officer; (8) Employee training on AML/CFT; (9) Customer Acceptance Policy; (10) Transaction monitoring and risk management systems."
    },
    {
        "question": "What is the regulatory framework for NBFCs' digital lending activities?",
        "answer": "RBI's Digital Lending Guidelines mandate: (1) All loan servicing through bank accounts of regulated entities; (2) No pass-through/back-to-back arrangements for loans; (3) First right to disbursal amount before Lending Service Provider (LSP) charges; (4) Key Fact Statement to be provided before loan agreement; (5) Explicit consent for data sharing with LSPs; (6) No automatic increase in credit limit without consent; (7) Cooling-off period mechanism; (8) Clear disclosure of all fees and charges; (9) Grievance redressal mechanism; (10) LSP code of conduct and oversight."
    },
    {
        "question": "What are the corporate governance requirements for NBFCs?",
        "answer": "Corporate governance norms include: (1) Board composition with adequate independent directors; (2) Minimum 4 board meetings per year; (3) Specialized committees: Audit, Risk Management, Nomination & Remuneration, IT Strategy; (4) Chief Compliance Officer appointment; (5) Internal audit function; (6) Risk management framework; (7) Fit and proper criteria for directors and key managerial personnel; (8) Disclosure requirements on website; (9) Related party transaction restrictions; (10) Succession planning for key positions."
    },
    {
        "question": "What is the regulatory framework for NBFC outsourcing?",
        "answer": "NBFCs must comply with outsourcing guidelines: (1) Board-approved outsourcing policy; (2) Risk assessment before outsourcing; (3) Due diligence on service providers; (4) Written contracts with clear SLAs; (5) Data confidentiality and security provisions; (6) Business continuity arrangements; (7) Right to audit by NBFC and RBI; (8) Regular monitoring and review; (9) Core management functions not to be outsourced; (10) Exit strategy in contracts; (11) Compliance with data localization requirements."
    },
    {
        "question": "What are the licensing requirements for different NBFC categories?",
        "answer": "Different NBFC categories have specific requirements: (1) NBFC-D: Rs.2 crore NOF, public deposit acceptance authorization; (2) NBFC-ND-SI: Rs.2 crore NOF, asset size >Rs.500 crore; (3) NBFC-IFC: Rs.300 crore NOF, 75% assets in infrastructure; (4) NBFC-MFI: Rs.5 crore NOF (Rs.2 crore for NE region), 85% assets in qualifying microfinance; (5) NBFC-Factor: Rs.5 crore NOF, 50% assets/income from factoring; (6) CIC: Rs.100 crore NOF, 90% in group companies; (7) IDF: Rs.300 crore NOF, 75% in infrastructure debt."
    },
    {
        "question": "What is the regulatory framework for NBFC-MFIs?",
        "answer": "NBFC-MFIs must comply with: (1) Minimum 85% of assets in qualifying microfinance loans; (2) Maximum loan per borrower: Rs.3 lakh (Rs.5 lakh for certain areas); (3) Household annual income cap: Rs.3 lakh (rural/semi-urban), Rs.4 lakh (urban); (4) Loan tenure: 24 months minimum for loans >Rs.30,000; (5) Margin cap: lower of 12% or 10% above cost of funds; (6) No prepayment penalty; (7) Fair practices on interest rates and collection; (8) Mandatory general credit card; (9) Grid-based lending with simplified KYC."
    },
    {
        "question": "What are the NBFC merger and acquisition guidelines?",
        "answer": "NBFC M&A process requires: (1) Prior RBI approval through detailed application; (2) Due diligence on financials, compliance, and litigations; (3) Valuation by independent valuers; (4) Satisfaction of fit and proper criteria by acquirer; (5) Post-merger NOF and CRAR compliance; (6) Creditor and depositor protection measures; (7) Scheme approval by NCLT; (8) Objection opportunity to stakeholders; (9) Reporting to RBI within 30 days of NCLT approval; (10) Integration plan including systems, employees, and branches."
    },
    {
        "question": "What are the penalties for non-compliance by NBFCs?",
        "answer": "Penalties under RBI Act, 1934: (1) Operating without registration: Imprisonment up to 5 years and/or fine up to Rs.5 lakh; (2) Violation of RBI directions: Penalty up to Rs.5,000 per day during default period; (3) Failure to furnish information: Penalty up to Rs.2 lakh; (4) Fraudulent deposit acceptance: Penalties under Prize Chits and Money Circulation Schemes (Banning) Act; (5) RBI can also cancel CoR, restrict activities, appoint administrator, or recommend winding up to NCLT for serious violations."
    },
    {
        "question": "What is the regulatory framework for NBFC securitization?",
        "answer": "Securitization norms include: (1) Minimum Holding Period: 9-12 months depending on loan type before securitization; (2) Minimum Retention Requirement (MRR): 5-10% of book value to be retained till maturity; (3) Reset of MRR on portfolio sale; (4) Risk weight on MRR portion: 100% or as per asset class; (5) Credit enhancement limited to MRR; (6) True sale criteria to be met; (7) Servicing rights and responsibilities; (8) Investor protection measures; (9) Disclosure and reporting requirements; (10) Restrictions on re-securitization."
    },
    {
        "question": "What are the key changes in the Scale Based Regulation (SBR) framework for NBFCs?",
        "answer": "SBR framework (effective October 2022) creates four layers: Base Layer (NBFC-BL): Asset size <Rs.1,000 crore, minimal regulation; Middle Layer (NBFC-ML): Rs.1,000-10,000 crore, moderate regulation; Upper Layer (NBFC-UL): Identified based on size/risk/interconnectedness, stringent regulation; Top Layer (NBFC-TL): Reserve layer, bank-like regulation. Progressive regulatory requirements include: governance, capital, leverage ratio, disclosure, concentration norms, and regulatory reporting based on layer. Aims to ensure proportionate regulation based on systemic risk."
    }
]


def create_langsmith_dataset(dataset_name="RBI-NBFC-FAQ-v1", limit=None):
    """Create a LangSmith dataset with RBI NBFC FAQ questions."""
    api_key = os.getenv("LANGSMITH_API_KEY")
    if not api_key:
        print("❌ Error: LANGSMITH_API_KEY not found")
        sys.exit(1)
    
    try:
        client = Client(api_key=api_key)
        print("✅ Connected to LangSmith")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    samples_to_use = RBI_FAQ_SAMPLES[:limit] if limit else RBI_FAQ_SAMPLES
    print(f"\n📊 Preparing dataset with {len(samples_to_use)} questions...")
    
    try:
        try:
            existing_dataset = client.read_dataset(dataset_name=dataset_name)
            print(f"⚠️  Dataset '{dataset_name}' already exists")
            user_input = input("Delete and recreate? (yes/no): ").strip().lower()
            if user_input == 'yes':
                client.delete_dataset(dataset_name=dataset_name)
                print("🗑️  Deleted existing dataset")
            else:
                print("❌ Aborted")
                sys.exit(0)
        except:
            pass
        
        dataset = client.create_dataset(
            dataset_name=dataset_name,
            description=f"RBI NBFC FAQ with {len(samples_to_use)} questions from April 23, 2025."
        )
        print(f"✅ Created dataset: {dataset_name}")
        
        print(f"\n📝 Adding {len(samples_to_use)} examples...")
        for idx, sample in enumerate(samples_to_use, 1):
            client.create_example(
                dataset_id=dataset.id,
                inputs={"question": sample["question"]},
                outputs={"expected_answer": sample["answer"]}
            )
            print(f"   Added {idx}/{len(samples_to_use)}: {sample['question'][:60]}...")
        
        print(f"\n✅ Successfully created dataset with {len(samples_to_use)} examples")
        print("🔗 View at: https://smith.langchain.com")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Create LangSmith dataset from RBI FAQ")
    parser.add_argument("--dataset-name", type=str, default="RBI-NBFC-FAQ-v1")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    
    print("=" * 80)
    print("RBI NBFC FAQ Dataset Builder")
    print("=" * 80)
    print(f"\nDataset: {args.dataset_name}")
    print(f"Questions: {args.limit if args.limit else 'All (23)'}\n")
    
    create_langsmith_dataset(dataset_name=args.dataset_name, limit=args.limit)


if __name__ == "__main__":
    main()
