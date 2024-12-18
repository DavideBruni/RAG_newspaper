from langchain.chains.query_constructor.base import AttributeInfo

document_content_description = "The text of a part of a newspaper article."
# Define allowed comparators list
allowed_comparators = [
    "$eq",  # Equal to (number, string, boolean)
    "$ne",  # Not equal to (number, string, boolean)
    "$gt",  # Greater than (number)
    "$gte",  # Greater than or equal to (number)
    "$lt",  # Less than (number)
    "$lte"  # Less than or equal to (number)
]

useful_attributes = ['author', 'date', 'section', 'type']

metadata_field_info = [
    AttributeInfo(
        name="author",
        description="The article's writer.",
        type="string"
    ),
    AttributeInfo(
        name="date",
        description="The article's date.",
        type="string"
    ),
    AttributeInfo(
        name="section",
        description="The article's section.",
        type="string"
    ),
    AttributeInfo(
        name="type",
        description="The article part type.",
        type="string"
    )
]

examples = [
    (
        'Oggi è il 18 Dicembre 2024. Fai un riassunto delle notizie di politica di oggi che parlano della Meloni',
        {
            "query": "Quali sono le notizie che parlano della Meloni?",
            "filter": "and(eq(\"date\", \"2024-12-18\"),eq(\"section\",\"politica\"))",
        },
    ),
    (
        'Oggi è il 15 Ottobre 2024. Quali sono i casi di cronaca di ieri raccontati da Mario Rossi?',
        {
            "query": "Quali sono i casi di cronaca?",
            "filter": "and(eq(\"date\", \"2024-10-14\"),eq(\"section\",\"cronaca\"),eq(\"author\",\"Mario Rossi\"))",
        },
    ),
    (
        'Oggi è il 20 Dicembre 2024. Cosa dicono gli articoli della sezione esteri parlano dell\'Italia?',
        {
            "query": "Quali articoli parlano dell'Italia?",
            "filter": "and(eq(\"date\", \"2024-12-20\"),eq(\"section\",\"esteri\"))",
        },
    ),
    (
        'Oggi è il 12 Settembre 2024. Quali articoli parlano di New York?',
        {
            "query": "Quali articoli parlano dell'Italia?",
            "filter": "eq(\"date\", \"2024-09-12\")",
        },
    ),
    (
        'Oggi è il 2 Dicembre 2024. Cosa dicono gli articoli di ploitica che parlano di Salvini?',
        {
            "query": "Cosa dicono gli articoli che parlano di Salvini?",
            "filter": "and(eq(\"date\", \"2024-12-02\"),eq(\"section\",\"politica\"))",
        },
    ),
]


system_prompt = """Sei un assistente per i compiti di risposta alle domande. 
        Istruzioni: 
            1. Familiarizzare con il contesto fornito.
            2. Se un documento non sembra rilevante rispetto alla domanda, omettilo dalla risposta. 
            3. Non fare mai riferimento a messaggi o fatti che non rientrano nel contesto. 
            4. Se non si è in grado di rispondere alla domanda, suggerire all'utente una domanda migliore o semplicemente dire che non si sa.
            5. Le risposte devono essere pertinenti.
           
            Nota:
                Non è possibile fare riferimento a un messaggio se non compare nel contesto."""

user_prompt = """
Istruzioni:
    1. Analizza il contesto fornito e rispondi alla domanda: i testi forniti sono tutti pertinenti! 
    2. La risposta deve basarsi esclusivamente sul contesto fornito: se non si è in grado di rispondere alla domanda, è sufficiente rispondere con “Non lo so”.
    3. La risposta deve includere i riferimenti agli [indici] dei documenti da cui è stata estratta, direttamente integrati nella risposta. Gli indici partono da 0. 

Ad esempio:
“Lorem Ipsum [0], lorem ipsum [1,4,5], lorem ipsum”.

Contesto: {context}
Domanda: {question}

Risposta:
"""
