from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from brokers.models import Category, Product
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for brokers app'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {
                'name': 'Mobil',
                'description': 'Kendaraan roda empat',
                'icon': 'fas fa-car',
                'color': '#3B82F6'
            },
            {
                'name': 'Motor',
                'description': 'Kendaraan roda dua',
                'icon': 'fas fa-motorcycle',
                'color': '#EF4444'
            },
            {
                'name': 'Truck',
                'description': 'Kendaraan angkut barang',
                'icon': 'fas fa-truck',
                'color': '#10B981'
            },
            {
                'name': 'Elektronik',
                'description': 'Perangkat elektronik',
                'icon': 'fas fa-laptop',
                'color': '#8B5CF6'
            },
            {
                'name': 'Furniture',
                'description': 'Perabot rumah tangga',
                'icon': 'fas fa-couch',
                'color': '#F59E0B'
            }
        ]

        self.stdout.write('Creating categories...')
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'✓ Created category: {category.name}')
            else:
                self.stdout.write(f'→ Category exists: {category.name}')

        # Get or create a user for products
        user, created = User.objects.get_or_create(
            username='seller1',
            defaults={
                'email': 'seller1@example.com',
                'first_name': 'John',
                'last_name': 'Seller'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write('✓ Created user: seller1')
        else:
            self.stdout.write('→ User exists: seller1')

        # Create sample products
        products_data = [
            {
                'title': 'Honda Civic 2020',
                'category': categories['Mobil'],
                'brand': 'Honda',
                'model': 'Civic',
                'condition': 'like_new',
                'attributes': {
                    'tahun': '2020',
                    'warna': 'Putih',
                    'transmisi': 'Automatic',
                    'bahan_bakar': 'Bensin',
                    'cc': '1500'
                },
                'price': Decimal('320000000'),
                'location_city': 'Jakarta',
                'location_province': 'DKI Jakarta',
                'contact_name': 'John Seller',
                'contact_phone': '081234567890',
                'description': 'Honda Civic 2020 kondisi sangat terawat, service record lengkap, interior bersih, eksterior mulus.'
            },
            {
                'title': 'Yamaha NMAX 2021',
                'category': categories['Motor'],
                'brand': 'Yamaha',
                'model': 'NMAX',
                'condition': 'good',
                'attributes': {
                    'tahun': '2021',
                    'warna': 'Biru',
                    'cc': '155',
                    'km': '15000'
                },
                'price': Decimal('28000000'),
                'location_city': 'Bandung',
                'location_province': 'Jawa Barat',
                'contact_name': 'John Seller',
                'contact_phone': '081234567890',
                'description': 'Yamaha NMAX 2021 kondisi terawat, sudah upgrade beberapa aksesoris.'
            },
            {
                'title': 'Laptop Gaming ASUS ROG',
                'category': categories['Elektronik'],
                'brand': 'ASUS',
                'model': 'ROG Strix',
                'condition': 'like_new',
                'attributes': {
                    'processor': 'Intel Core i7',
                    'ram': '16GB',
                    'ssd': '512GB',
                    'vga': 'RTX 3060'
                },
                'price': Decimal('18000000'),
                'location_city': 'Surabaya',
                'location_province': 'Jawa Timur',
                'contact_name': 'John Seller',
                'contact_phone': '081234567890',
                'description': 'Laptop gaming ASUS ROG kondisi mulus, cocok untuk gaming dan editing.'
            },
            {
                'title': 'Sofa 3 Dudukan',
                'category': categories['Furniture'],
                'brand': 'IKEA',
                'model': 'KIVIK',
                'condition': 'good',
                'attributes': {
                    'material': 'Fabric',
                    'warna': 'Abu-abu',
                    'ukuran': '228x95x83 cm'
                },
                'price': Decimal('3500000'),
                'location_city': 'Medan',
                'location_province': 'Sumatera Utara',
                'contact_name': 'John Seller',
                'contact_phone': '081234567890',
                'description': 'Sofa IKEA KIVIK 3 dudukan, kondisi bagus, nyaman untuk keluarga.'
            }
        ]

        self.stdout.write('Creating products...')
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                title=product_data['title'],
                seller=user,
                defaults=product_data
            )
            if created:
                self.stdout.write(f'✓ Created product: {product.title}')
            else:
                self.stdout.write(f'→ Product exists: {product.title}')

        self.stdout.write(self.style.SUCCESS('\n🎉 Sample data created successfully!'))
        self.stdout.write(f'Created {Category.objects.count()} categories')
        self.stdout.write(f'Created {Product.objects.count()} products')
        self.stdout.write('\nYou can now access the admin at http://localhost:8000/admin/')
        self.stdout.write('Username: putra | Password: [your password]')
