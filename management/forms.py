from django import forms
from .models import Warehouses
from geopy.geocoders import Nominatim

class WarehouseAdminForm(forms.ModelForm):
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),  # Make the field bigger
        help_text="Enter the address to calculate latitude and longitude.",)

    class Meta:
        model = Warehouses
        fields = ['name', 'capacity', 'lat', 'long']  # Exclude 'address' from the database fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.lat and self.instance.long:
            geolocator = Nominatim(user_agent="warehouse_geocoder")
            location = geolocator.reverse((self.instance.lat, self.instance.long))
            if location:
                self.fields['address'].initial = location.address