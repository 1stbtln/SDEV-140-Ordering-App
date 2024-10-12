## **Pizza Ordering App User Manual**

Welcome to the **Pizza Ordering App**! This application allows you to easily order your favorite pizza with customizable sizes and toppings. Follow the steps below to use the app effectively.

---

### **1. Launching the App**

To launch the app:
- Double-click on the application file or run the following command in your terminal:
  ```bash
  python app.py
  ```

The app will open with a clean and simple interface ready for your pizza order.

---

### **2. Main Screen (Order Page)**

Once the app is open, you will see the **Order Page**, where you can begin customizing your pizza.

#### **2.1 Selecting Pizza Size**
- There is a dropdown menu labeled "Select Pizza Size".
- Choose from three available sizes:
  - Small
  - Medium (default)
  - Large

#### **2.2 Selecting Toppings**
- Below the pizza size dropdown, there is a list of available toppings.
- Select your favorite toppings by clicking on them in the list. You can choose multiple toppings.
  - Available toppings include:
    - Cheese
    - Pepperoni
    - Mushrooms
    - Onions
    - Sausage
    - Bacon
    - Green Peppers
    - Olives

#### **2.3 Logo**
- The pizza company logo is displayed above the order form.

#### **2.4 Confirming Your Order**
- Once you've chosen your pizza size and toppings, click on the **Confirm Order** button to proceed.
- If you don’t select any toppings, the app will show a warning message asking you to choose at least one topping.

#### **2.5 Exit the App**
- To exit the app at any time, click the **Exit** button. If you attempt to exit, the app will confirm if you truly want to quit.

---

### **3. Summary Screen (Order Summary Page)**

Once you confirm your order, the app will display the **Order Summary**.

#### **3.1 Pizza Image**
- At the top of this page, you will see an image of a pizza.

#### **3.2 Order Details**
- Below the image, your order details will be displayed:
  - Selected pizza size.
  - Selected toppings.
  - Total price (based on the size and the number of toppings).

#### **3.3 Place Order**
- To finalize your order, click the **Place Order** button. This will place the order and reset the app for another new order.

#### **3.4 Return to Order Page**
- If you need to make changes to your order, click the **Back to Order** button to return to the main screen and adjust your order.

---

### **4. Resetting and Starting a New Order**

After placing an order, the app automatically resets to default settings:
- Pizza size is set back to "Medium".
- No toppings are selected.

You can place a new order immediately or exit the app.

---

### **5. Troubleshooting**

- **Image Load Error**: If an image fails to load, ensure that the image files are correctly located in the project directory with the exact filenames:
  - `img1.png` (for the pizza image)
  - `img2.png` (for the logo)
  
- **No Toppings Selected**: The app will warn you if you try to place an order without selecting toppings.

---
