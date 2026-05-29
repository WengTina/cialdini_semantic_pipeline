#Cialdini’s six Principles

CIALDINI_LEXICON = {
    "reciprocity": [
        "reward", "bonus", "gift", "free", "refund", "claim",
        "compensation", "offer", "benefit", "cashback", "prize",
        "redeem", "complimentary", "voucher", "special offer"
    ],

    "liking": [
        "dear customer", "valued customer", "valued member",
        "trusted", "appreciate", "thank you", "friend",
        "partner", "loyal customer", "exclusive for you",
        "we care", "welcome back", "dear user"
    ],

    "social_proof": [
        "many users", "everyone", "all employees", "your colleagues",
        "trusted by", "popular", "widely used", "customers have",
        "people are", "recommended by", "most users",
        "members have", "others have", "users have already"
    ],

    "authority": [
        "admin", "administrator", "security team", "support team",
        "it department", "official", "bank", "government",
        "manager", "ceo", "compliance team", "account department",
        "system notice", "microsoft", "paypal", "google", "amazon",
        "security department", "billing department", "official notice"
    ],

    "scarcity": [
        "urgent", "immediately", "as soon as possible", "act now",
        "limited time", "expires", "deadline", "last chance",
        "final notice", "within 24 hours", "today only",
        "suspended", "locked", "terminate", "restricted",
        "account closure", "before it expires"
    ],

    "commitment_consistency": [
        "confirm", "verify", "continue", "renew", "update",
        "complete", "proceed", "maintain", "follow the steps",
        "validate", "activate", "review your account",
        "complete the process", "confirm your identity",
        "verify your account", "update your information"
    ]
}

CIALDINI_PRINCIPLES = list(CIALDINI_LEXICON.keys())

CANDIDATE_LABELS = [
    "reciprocity",
    "liking",
    "social proof",
    "authority",
    "scarcity",
    "commitment and consistency"
]

LABEL_TO_PRINCIPLE = {
    "reciprocity": "reciprocity",
    "liking": "liking",
    "social proof": "social_proof",
    "authority": "authority",
    "scarcity": "scarcity",
    "commitment and consistency": "commitment_consistency"
}