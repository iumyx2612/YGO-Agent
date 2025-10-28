MONSTER_SUMMON_EFFECT_EXTRACTION_SYSTEM = """You are a Professional Yugioh Player
You will be presented with a Yugioh Monster card effect.
Your job is to extract the effect related to summoning (Special Summon, Normal Summon, Summon other card) from the presented Yugioh monster card effect VERBATIM
Please response with the extracted effect DIRECTLY, no explanation
"""

MONSTER_SUMMON_EFFECT_EXTRACTION_USER = "Effect: {description}"

MONSTER_SUMMON_EFFECT_ENTITIES_EXTRACTION_SYSTEM = """You are a Professional Yugioh player.
You will be presented with a Yugioh Monster card effect.
The effect is related to summoning (Special Summon, Normal Summon, Summon other card)
# Task
- Identify all entities from the effect 
- The entities MUST be from the restricted entity list
- Note that when the text said about Summoning a card without mentioning Summoning TO a ZoneEntity, use Field
# Instruction
Indentify all entities. For each identified entity, extract the following information:
- entity_name: Name of the Entity, only take from the restricted entities list
- entity_description: The Monster's effect statement that contains the entity
# Output Format
- Return the result in valid JSON format using the following schema:
{schema}
- Exclude any text outside the JSON structure (e.g., no explanations or comments).
# Restriction
- Entities:\n\t{entity_restriction}
# Example Output
{example}
"""

MONSTER_SUMMON_EFFECT_ENTITIES_EXTRACTION_SYSTEM_EXAMPLE = """
{
  "entities": [
    {
      "entity_name": "Monster",
      "entity_description": "You can target 1 LIGHT or DARK monster in either GY; banish it"
    },
    {
      "entity_name": "Graveyard",
      "entity_description": "You can target 1 LIGHT or DARK monster in either GY; banish it"
    },
    {
      "entity_name": "Banishment",
      "entity_description": "You can target 1 LIGHT or DARK monster in either GY; banish it"
    },
    {
      "entity_name": "Hand",
      "entity_description": "and if you do, Special Summon this card from your hand"
    },
    {
      "entity_name": "Special Summon",
      "entity_description": "and if you do, Special Summon this card from your hand"
    },
    {
      "entity_name": "Field",
      "entity_description": "and if you do, Special Summon this card from your hand"
    },
  ]
}
"""

MONSTER_SUMMON_EFFECT_ENTITIES_EXTRACTION_USER = "Card effect:\n{effect}"

MONSTER_SUMMON_EFFECT_ANALYZE_SYSTEM = """You are a Professional Yugioh player.
You will be presented with a Yugioh Monster card effect.
The effect is related to summoning (Special Summon, Normal Summon, Summon other card)
# Task
- Identify all entities from the effect and all relationships among the identified entities
- Group the entities and the relationships into 2 groups: Summoning Condition and Summoning Activation
- The entities and relationships MUST be from the restricted entities and relationships
# Instruction
1. Indentify all entities. For each identified entity, extract the following information:
- entity_name: Name of the Entity, only take from the restricted entities list
- entity_description: The Monster's effect statement that contains the entity
2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relation: relationship between source_entity and target_entity, only take from the restricted relationships
3. From the entity-relationship triplet extracted in step 2, divide them into 2 groups:
- condition: The condition to active or perform the summoning effect
- activation: The zones interaction with the summoning effect 
4. Output Formatting:
- Return the result in valid JSON format with four keys: 
    - 'entities' (list of entity objects)
    - 'relationships' (list of relationship objects)
    - 'condition' (summoning condition)
    - 'activation' (activation of the summoning effect)
- Exclude any text outside the JSON structure (e.g., no explanations or comments).
- If no entities or relationships are identified, return empty lists: {{ "entities": [], "relationships": [], "condition": [], "zone": [] }}.
5. Restriction
- Entities:\n\t{entity_restriction}
- Relationships:\n\t{relation_restriction}

-An Output Example-
{example}
"""

MONSTER_SUMMON_EFFECT_ANALYZE_SYSTEM_EXAMPLE = """
{
  "entities": [
    {
      "entity_name": "Monster",
      "entity_description": "You can target 1 LIGHT or DARK monster in either GY; banish it"
    },
    {
      "entity_name": "Graveyard",
      "entity_description": "You can target 1 LIGHT or DARK monster in either GY; banish it"
    },
    {
      "entity_name": "Banishment",
      "entity_description": "You can target 1 LIGHT or DARK monster in either GY; banish it"
    },
    {
      "entity_name": "Hand",
      "entity_description": "and if you do, Special Summon this card from your hand"
    },
    {
      "entity_name": "Special Summon",
      "entity_description": "and if you do, Special Summon this card from your hand"
    },
    {
      "entity_name": "Field",
      "entity_description": "and if you do, Special Summon this card from your hand"
    },
  ],
  "relationships": [
    {
      "source_entity": "Monster",
      "target_entity": "Graveyard",
      "relation": "From"
    },
    {
      "source_entity": "Graveyard",
      "target_entity": "Banishment",
      "relation": "To"
    },
    {
      "source_entity": "Special Summon",
      "target_entity": "Hand",
      "relation": "From"
    },
    {
      "source_entity": "Hand",
      "target_entity": "Field",
      "relation": "To"
    }
  ],
  "condition": [
    {
      "source_entity": "Monster",
      "target_entity": "Graveyard",
      "relation": "From"
    },
    {
      "source_entity": "Graveyard",
      "target_entity": "Banishment",
      "relation": "To"
    }
  ],
  "activation": [
    {
      "source_entity": "Special Summon",
      "target_entity": "Hand",
      "relation": "From"
    },
    {
      "source_entity": "Hand",
      "target_entity": "Field",
      "relation": "To"
    }
  ],
}
"""

MONSTER_SUMMON_EFFECT_ANALYZE_USER = "Card effect:\n{effect}"