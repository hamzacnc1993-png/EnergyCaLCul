from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class SolarCalculatorApp(App):

  def build(self):
    self.title = "Solar PR Calculator"

    # تخطيط يملأ الشاشة بأحجام عملاقة
    layout = GridLayout(cols=1, padding=15, spacing=12, size_hint=(1, 1))

    # 1. عنوان التطبيق بحجم عملاق جداً
    title_label = Label(
        text="Solar PR Calculator",
        font_size=42,
        bold=True,
        color=(0.1, 0.45, 0.9, 1),
        size_hint_y=None,
        height=90,
    )
    layout.add_widget(title_label)

    # دالة لإنشاء حقول عملاقة وواضحة جداً
    def add_field(label_text, hint):
      lbl = Label(
          text=label_text,
          font_size=40,
          bold=True,
          color=(0.2, 0.2, 0.2, 1),
          size_hint_y=None,
          height=60,
      )
      txt = TextInput(
          hint_text=hint,
          multiline=False,
          input_type="number",
          font_size=42,
          size_hint_y=None,
          height=90,  # خانة إدخال عملاقة
      )
      layout.add_widget(lbl)
      layout.add_widget(txt)
      return txt

    # 2. حقول الإدخال (تدعم النقطة والفاصلة)
    self.cap_input = add_field("Nominal Capacity (MW):", "e.g. 50.5 or 50,5")
    self.energy_input = add_field(
        "Produced Energy (MWh):", "e.g. 85000.75"
    )
    self.irr_input = add_field("Solar Irradiation (MJ/m²):", "e.g. 1800.5")

    # 3. زر الحساب بحجم عملاق جداً
    calc_btn = Button(
        text="Calculate PR",
        background_normal="",
        background_color=(0.1, 0.5, 0.9, 1),
        color=(1, 1, 1, 1),
        font_size=42,
        bold=True,
        size_hint_y=None,
        height=150,  # زر عملاق
    )
    calc_btn.bind(on_press=self.calculate)
    layout.add_widget(calc_btn)

    # 4. خانة النتيجة عملاقة جداً بخط أبيض بارز تملأ الشاشة
    self.result_box = Button(
        text="Enter values & tap Calculate",
        background_normal="",
        background_color=(0.08, 0.3, 0.6, 1),  # خلفية زرقاء داكنة
        color=(1, 1, 1, 1),  # كتابة باللون الأبيض الصريح
        font_size=42,
        bold=True,
        size_hint_y=None,
        height=140,  # بطاقة نتيجة عملاقة جداً
    )
    layout.add_widget(self.result_box)

    return layout

  def calculate(self, instance):
    try:
      # دعم استخدام الفاصلة أو النقطة للأرقام العشرية
      c = self.cap_input.text.replace(",", ".")
      e = self.energy_input.text.replace(",", ".")
      i = self.irr_input.text.replace(",", ".")

      if not c or not e or not i:
        self.result_box.text = "Error: Fill all fields!"
        return

      p_nom = float(c)
      energy = float(e)
      irr_mj = float(i)

      if p_nom <= 0 or energy < 0 or irr_mj < 0:
        self.result_box.text = "Error: Positive values only!"
        return

      p_nom_kw = p_nom * 1000
      energy_kwh = energy * 1000
      irr_kwh = irr_mj / 3.6

      yf = energy_kwh / p_nom_kw
      yr = irr_kwh / 1.0

      if yr == 0:
        self.result_box.text = "Error: Irradiation cannot be zero!"
        return

      pr = (yf / yr) * 100
      self.result_box.text = (
          f"Irradiation: {irr_kwh:,.1f} kWh/m²\nPR: {pr:.2f}%"
      )

    except ValueError:
      self.result_box.text = "Error: Use valid numbers!"


if __name__ == "__main__":
  SolarCalculatorApp().run()
