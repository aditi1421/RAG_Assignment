from faker import Faker
import uuid
import random
import pandas as pd

fake = Faker()
Faker.seed(42) #Hitchhiker's Guide to Galaxy!
random.seed(42)

# Templates for generating random about, ideas, bios, notes & industries
idea_templates = [
    "Building a {industry} platform that helps {audience} {benefit}.",
    "Creating AI-powered tools for {audience} to improve {benefit}.",
    "Developing {product} to solve {problem} in {industry}.",
    "A {industry} solution that automates {process} for {audience}.",
    "Connecting {audience} with {product} through a {industry} marketplace.",
    "Helping {audience} in {industry} {benefit} with {product}.",
    "A new way for {audience} to access {service} in {industry}.",
    "Providing {audience} with {service} that drives {benefit}.",
    "Simplifying {process} in {industry} using {product}.",
    "On-demand {service} for {audience} in the {industry} space.",
    "A platform that connects {audience} and {audience} through {service}.",
    "Personalized {product} for {audience} to {benefit}.",
    "Smart {product} that solves {problem} for {audience}."
]

about_templates = [
    "{name} has a background in {field} with over {years} years of experience. "
    "They have worked at {company} and specialize in {skills}. "
    "Their work has led to {outcome}.",

    "With expertise in {skills}, {name} has previously contributed to {company}. "
    "They are passionate about {field} and focus on delivering {outcome}.",

    "{name} combines experience in {field} with strong skills in {skills}. "
    "They have built solutions for {audience} and achieved {outcome}."
]
note_templates = [
    "Follow up with {company} about partnership.",
    "Raised interest from {company} investors.",
    "Currently prototyping {product} for {audience}.",
    "Needs support with {process} and scaling.",
    "Strong traction in {industry}, next milestone is growth stage.",
    "Pilot project with {company} shows {outcome}.",
    "Considering expansion into {industry} markets.",
    "Potential collaboration with {company} on {service}.",
    "Seeking advisors for {audience}-focused growth.",
    "Positive early feedback from {audience} using {product}."
]

industries = ["healthcare", "AI", "robotics", "fintech", "edtech", "climate", "Marketing"]
audiences = ["doctors", "teachers", "small businesses", "patients", "consumers", "developers"]
benefits = ["reduce costs", "save time", "improve accuracy", "scale faster", "increase access"]
products = ["mobile app", "platform", "AI system", "robotic assistant"]
problems = ["diagnosis delays", "education gaps", "financial fraud", "logistics inefficiency"]
processes = ["data entry", "reporting", "patient care", "fraud detection"]
service = [
    "mentorship", "legal advice", "analytics", "fundraising", 
    "delivery", "marketing support", "cloud hosting", 
    "supply chain optimization", "customer support", "training"
]


fields = ["computer science", "biotechnology", "finance", "product design", "engineering"]
skills_list = ["machine learning", "robotics", "UI/UX design", "cloud systems", "AI","data science"]
companies = ["Google", "Tesla", "Microsoft", "Neuralink","Apple","Stripe", "OpenAI", "Amazon", "AntlerIndia"]
outcomes = ["faster product launches", "reduced errors", "scalable systems", "impactful research"]



def generate_idea():
    template = random.choice(idea_templates)
    return template.format(
        industry=random.choice(industries),
        audience=random.choice(audiences),
        benefit=random.choice(benefits),
        product=random.choice(products),
        problem=random.choice(problems),
        process=random.choice(processes),
        service=random.choice(service)
    )

def generate_about(name):
    template = random.choice(about_templates)
    return template.format(
        name=name,
        field=random.choice(fields),
        years=random.randint(3, 12),
        company=random.choice(companies),
        skills=random.choice(skills_list),
        outcome=random.choice(outcomes),
        audience=random.choice(audiences)
    )
email_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]

def generate_email(name):
    username = name.lower().replace(" ", ".").replace("'", "")
    domain = random.choice(email_domains)
    return f"{username}@{domain}"

def generate_notes():
    if random.random() > 0.7:  # 30% chance of having notes
        return random.choice(note_templates).format(
            company=random.choice(companies),
            product=random.choice(products),
            audience=random.choice(audiences),
            process=random.choice(processes),
            industry=random.choice(industries),
            outcome=random.choice(outcomes),
            service=random.choice(["mentorship","legal advice","analytics","fundraising","delivery"])
        )
    return ""

roles = ["Founder","Co-Founder", "Engineer","PM","Investor","Other"]
stages = ["none","pre-seed","seed","series A","growth"]
keywords = ["healthcare","AI","marketplace","robotics","fintech",
            "consumer","b2b","Crypto","Edtech","Legal","BioTech","Logistics"]


rows = []

for _ in range(700):
    name = fake.name()
    row = {
        "id":str(uuid.uuid4()),
        "founder_name": name,
        "email": generate_email(name),
        "role": random.choice(roles),
        "company": fake.company(),
        "location": f"{fake.city()}, {fake.country()}",
        "idea":generate_idea(),
        "about":generate_about(name),
        "keywords":", ".join(random.sample(keywords, 3)),
        "stage": random.choice(stages),
        "linked_in": f"https://linkedin.com/in/{fake.user_name()}",
        "notes": generate_notes()
    }

    rows.append(row)

# Convert list of dicts → DataFrame
df = pd.DataFrame(rows)

df.to_csv("founders.csv", index=False)
print("✅ CSV with 700 rows created: founders.csv")
