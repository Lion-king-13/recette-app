import motor2
import pytest


@pytest.fixture()
def database():
    conn = motor2.create_db_connection(":memory:")
    motor2.create_tables(conn)
    yield conn
    conn.close()


def test_add_recipe(database):
    motor2.add_recipe(
        database,
        "dessert",
        "Tarte aux fraises",
        8,
        45,
        "Lait, oeufs, fraise",
        "Faire la pâte puis la crème et tout assembler",
    )
    desserts = motor2.get_recipes_by_category(database, "dessert")
    assert len(desserts) == 1
    assert desserts[0][1] == "Tarte aux fraises"


def test_get_recipes_by_category(database):
    motor2.add_recipe(
        database,
        "dessert",
        "Flan",
        4,
        75,
        "Oeuf, sucre, lait",
        "Tout mélanger puis cuire",
    )
    motor2.add_recipe(
        database,
        "plat",
        "Boeuf Bourguignon",
        4,
        50,
        "Boeuf, légumes, vin",
        "Cuire le boeuf et les légumes en sauce",
    )

    plats = motor2.get_recipes_by_category(database, "plat")
    assert len(plats) == 1
    assert plats[0][1] == "Boeuf Bourguignon"

    desserts = motor2.get_recipes_by_category(database, "dessert")
    assert len(desserts) == 1
    assert desserts[0][1] == "Flan"


def test_get_random_recipe(database):
    motor2.add_recipe(
        database,
        "plat",
        "Boeuf Bourguignon",
        4,
        50,
        "Boeuf, légumes, vin",
        "Cuire le boeuf",
    )
    motor2.add_recipe(
        database,
        "entree",
        "Pâtes Pesto",
        2,
        30,
        "Pâtes, pesto, tomate, mozzarella",
        "Cuire et mélanger",
    )
    motor2.add_recipe(
        database,
        "dessert",
        "Flan",
        4,
        75,
        "Oeuf, sucre, lait",
        "Tout mélanger puis cuire",
    )

    recipe = motor2.get_random_recipe(database)
    assert recipe is not None
    assert recipe[1] in ["Boeuf Bourguignon", "Pâtes Pesto", "Flan"]


def test_delete_recipe(database):
    motor2.add_recipe(
        database,
        "entree",
        "Pâtes Pesto",
        2,
        30,
        "Pâtes, pesto, tomate, mozzarella",
        "Cuire et mélanger",
    )
    recipes = motor2.get_recipes_by_category(database, "entree")
    assert len(recipes) == 1

    recipe_id = recipes[0][0]
    motor2.delete_recipe(database, "entree", recipe_id)

    recipes = motor2.get_recipes_by_category(database, "entree")
    assert len(recipes) == 0


def test_add_recipe_invalid_table(database):
    with pytest.raises(ValueError, match="Table inconnue"):
        motor2.add_recipe(
            database, "boisson", "Coca", 1, 0, "Eau, sucre", "Verser dans un verre"
        )


def test_get_recipes_invalid_category(database):
    with pytest.raises(ValueError, match="Catégorie inconnue"):
        motor2.get_recipes_by_category(database, "soupe")


def test_delete_invalid_table(database):
    with pytest.raises(ValueError, match="Table inconnue"):
        motor2.delete_recipe(database, "salade", 1)


def test_multiple_recipes(database):
    motor2.add_recipe(
        database, "entree", "Salade", 2, 10, "Laitue, vinaigrette", "Mélanger"
    )
    motor2.add_recipe(database, "entree", "Soupe", 4, 20, "Légumes", "Cuire")
    recettes = motor2.get_recipes_by_category(database, "entree")
    assert len(recettes) == 2
