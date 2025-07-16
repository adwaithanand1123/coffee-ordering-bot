import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

class JavaAssistant:
    def __init__(self):
        self.phase = "welcome"
        self.current_order = {
            "beverage": None,
            "variety": None,
            "portion": None,
            "sweetness": None,
            "dairy": None,
        }
        self.order_history = []
        self.drinks_menu = {
            "Coffee": ["Espresso", "Latte", "Cappuccino", "Americano", "Flat White", "Mocha"],
            "Tea": ["English Breakfast", "Earl Grey", "Green Tea", "Chai"],
            "Specialties": ["Caramel Macchiato", "Vanilla Latte", "Hazelnut Mocha"]
        }
        self.messages = {
            "welcome": "Hi there! Ready for some caffeine? What'll it be today? |wave",
            "variety_prompt": "Got it, {beverage}! Which specific variety? |open_hand",
            "size_prompt": "{variety} {beverage} - excellent! What portion? Small/Medium/Large? |open_hand",
            "sweetness_prompt": "How sweet? None/Light/Regular/Extra? |thinking",
            "dairy_prompt": "Dairy preference? Full/Skim/Oat/Soy/Almond? |open_hand",
            "verify_order": "Confirming: {portion} {variety} {beverage}, {sweetness} sweet, {dairy}. Correct? |nod",
            "additional_order": "Another beverage? |open_hand",
            "payment_prompt": "Total: £{total_cost:.2f}. Ready to pay? |point",
            "confused": "Sorry, could you repeat that? |thinking"
        }
        self.pricing = {
            "small": 2.89,
            "medium": 3.49,
            "large": 3.99
        }

    def compute_total(self):
        return sum(self.pricing[item["portion"]] for item in self.order_history)

    def interpret_input(self, user_text):
        user_text = user_text.lower().strip()
        beverage_map = {
            "coffee": ["coffee", "brew", "joe"],
            "tea": ["tea", "chai", "brew"],
            "specialties": ["special", "signature"]
        }
        varieties = [v.lower() for cat in self.drinks_menu.values() for v in cat]
        sizes = ["small", "medium", "large"]
        sweetness_levels = ["none", "light", "regular", "extra"]
        dairy_options = ["full", "skim", "oat", "soy", "almond"]

        beverage = variety = portion = sweetness = dairy = None

        # Beverage detection
        for cat, terms in beverage_map.items():
            if any(t in user_text for t in terms):
                beverage = cat
                break
        
        # Attribute extraction
        if any(v in user_text for v in varieties):
            variety = next(v for v in varieties if v in user_text)
        if any(s in user_text for s in sizes):
            portion = next(s for s in sizes if s in user_text)
        if any(sw in user_text for sw in sweetness_levels):
            sweetness = next(sw for sw in sweetness_levels if sw in user_text)
        if any(d in user_text for d in dairy_options):
            dairy = next(d for d in dairy_options if d in user_text)

        return beverage, variety, portion, sweetness, dairy

    def generate_response(self, user_input):
        user_input = user_input.lower().strip()

        if self.phase == "welcome":
            self.phase = "order_processing"
            return self.messages["welcome"]

        if self.phase == "order_processing":
            beverage, variety, portion, sweetness, dairy = self.interpret_input(user_input)

            # Update order details progressively
            if beverage and not self.current_order["beverage"]:
                self.current_order["beverage"] = beverage
            if variety and not self.current_order["variety"]:
                self.current_order["variety"] = variety
            if portion and not self.current_order["portion"]:
                self.current_order["portion"] = portion
            if sweetness and not self.current_order["sweetness"]:
                self.current_order["sweetness"] = sweetness
            if dairy and not self.current_order["dairy"]:
                self.current_order["dairy"] = dairy

            # Progressive questioning
            if not self.current_order["variety"]:
                if self.current_order["beverage"]:
                    return self.messages["variety_prompt"].format(
                        beverage=self.current_order["beverage"]
                    )
            if not self.current_order["portion"]:
                return self.messages["size_prompt"].format(
                    beverage=self.current_order["beverage"],
                    variety=self.current_order["variety"]
                )
            if not self.current_order["sweetness"]:
                return self.messages["sweetness_prompt"]
            if not self.current_order["dairy"]:
                return self.messages["dairy_prompt"]

            # Order verification
            if all(self.current_order.values()):
                self.phase = "order_verification"
                return self.messages["verify_order"].format(
                    beverage=self.current_order["beverage"],
                    variety=self.current_order["variety"],
                    portion=self.current_order["portion"],
                    sweetness=self.current_order["sweetness"],
                    dairy=self.current_order["dairy"]
                )

        if self.phase == "order_verification":
            if user_input.startswith(("y", "yes")):
                self.order_history.append(self.current_order.copy())
                self.current_order = {k: None for k in self.current_order}
                self.phase = "followup_order"
                return self.messages["additional_order"]
            elif user_input.startswith(("n", "no")):
                self.phase = "order_processing"
                return "Let's restart your order!"

        if self.phase == "followup_order":
            if user_input.startswith(("y", "yes")):
                self.phase = "order_processing"
                return "What else would you like?"
            elif user_input.startswith(("n", "no")):
                total_cost = self.compute_total()
                self.phase = "payment_processing"
                return self.messages["payment_prompt"].format(total_cost=total_cost)

        if self.phase == "payment_processing":
            if user_input.startswith(("y", "yes")):
                self.phase = "complete"
                return "Payment received! Your order is being prepared. |finished"
            elif user_input.startswith(("n", "no")):
                self.phase = "complete"
                return "Order noted. Please pay at pickup. |finished"

        if self.phase == "complete":
            return "Thanks for visiting! Enjoy your day. |wave"

        return self.messages["confused"]


def run_chat():
    assistant = JavaAssistant()
    print("Java Assistant: Welcome to our coffee shop!")
    while True:
        user_input = input("You: ")
        response = assistant.generate_response(user_input)
        print(f"Java Assistant: {response}")
        if assistant.phase == "complete":
            break


if __name__ == "__main__":
    run_chat()