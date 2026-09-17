from django import forms 
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_desc', 'item_price', 'item_image']
        widgets = {
            "item_name": forms.TextInput(attrs={"placeholder": "e.g Margherita Pizza"}),
            "item_desc": forms.TextInput(attrs={"placeholder": "e.g Cheesy tomato base pizza"}),
            "item_price": forms.NumberInput(attrs={"placeholder": "e.g 49.49"}),
            "item_image": forms.URLInput(attrs={"placeholder": "e.g https://example.com/pizza.jpg"}),
        }

    def clean_item_price(self):
        price = self.cleaned_data["item_price"]

        if price < 0:
            raise forms.ValidationError("Price cannot be negative")

        return price

    def clean(self):
        cleaned = super().clean()
        name = cleaned.get("item_name")
        desc = cleaned.get("item_desc")
        
        # 1. Fixed: Changed .low() to .lower()
        if name and desc and name.lower() in desc.lower():
            self.add_error("item_desc", "Description should add new info beyond the item name.")
            
        # 2. Fixed: Removed the trailing space and dot after 'cleaned'
        return cleaned
