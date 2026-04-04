from ddgs import DDGS

def test_chat():
    try:
        with DDGS() as ddgs:
            print("Testing DDGS Chat...")
            for r in ddgs.chat("Hello, who are you?", model="gpt-4o-mini"): # default models vary
                print(r, end="", flush=True)
            print("\nSuccess!")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    test_chat()
