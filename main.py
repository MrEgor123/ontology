from owlready2 import *
import os

# Загружаем онтологию
onto_path.append(os.getcwd())
ontology_file = "gadgets_ontology.owl"
onto = get_ontology(ontology_file).load()

# Проверяем, есть ли класс "Гаджет"
if hasattr(onto, "Гаджет"):
    GadgetClass = onto.Гаджет
else:
    raise ValueError("Класс 'Гаджет' не найден в онтологии!")

# Функция для удаления префикса "gadgets_ontology."
def clean_name(value):
    return str(value).split(".")[-1] if "." in str(value) else str(value)

# Вывод всех экземпляров гаджетов и их свойств (для отладки)
print("\n=== Загруженные гаджеты и их свойства ===")
for gadget in GadgetClass.instances():
    print(f"\nГаджет: {gadget.name}")
    if hasattr(gadget, "имеет_цену") and gadget.имеет_цену:
        print(f"  Цена: {[clean_name(x) for x in gadget.имеет_цену]}")
    if hasattr(gadget, "производится_брендом") and gadget.производится_брендом:
        print(f"  Бренд: {[clean_name(x) for x in gadget.производится_брендом]}")
    print(f"  Тип: {[clean_name(cls.name) for cls in gadget.is_a]}")

def recommend_gadget(price_category, brand, gadget_type):
    """
    Фильтрует гаджеты по ценовой категории, бренду и типу.
    """
    recommendations = []
    for gadget in GadgetClass.instances():
        try:
            # Получаем очищенные значения
            price_values = [clean_name(x) for x in gadget.имеет_цену] if hasattr(gadget, "имеет_цену") and gadget.имеет_цену else []
            brand_values = [clean_name(x) for x in gadget.производится_брендом] if hasattr(gadget, "производится_брендом") and gadget.производится_брендом else []
            type_values = [clean_name(cls.name) for cls in gadget.is_a]

            # Фильтрация
            if price_category not in price_values:
                continue
            if brand not in brand_values:
                continue
            if gadget_type not in type_values:
                continue

            recommendations.append(gadget)

        except Exception as e:
            print(f"Ошибка обработки {gadget.name}: {e}")

    return recommendations

def main():
    print("\nВведите ценовую категорию (Бюджетный, Средний, Дорогой):")
    price_category = input().strip()

    print("Введите бренд (Apple, Samsung, Lenovo, Asus):")
    brand = input().strip()

    print("Введите тип гаджета (Ноутбук, Смартфон, Планшет):")
    gadget_type = input().strip()

    results = recommend_gadget(price_category, brand, gadget_type)

    if results:
        print("\nРекомендуемые гаджеты:")
        for gadget in results:
            print(gadget.name)
    else:
        print("\nНет подходящих гаджетов.")

if __name__ == "__main__":
    main()
