import unittest
from app import app
class TestApp(unittest.TestCase):
    def setUp(self):
        self.client=app.test_client()
        self.client.testing=True
    def index(self):
        response=self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Login',response.data)
    def test_signup(self):
        data={'name':'tahseen','email':'t1dg5rd34r4564@gmail.com','password':"pass",'confirm_password':"pass"}
        response=self.client.post('/signup',data=data,content_type='multipart/form-data')
        self.assertEqual(response.status_code,302)
        self.assertIn(b'login',response.data)
    def test_login(self):
        data={'name':'khushal','email':'t1a2e3dr456@gmail.com','password':"pass",'confirm_password':"pass"}
        response=self.client.post('/signup',data=data,content_type='multipart/form-data')
        data = {'email': 't1a2e3dr456@gmail.com', 'password': 'pass'}
        response = self.client.post('/login', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'home', response.data)
    def test_add_electronics(self):
        data={'name_product' : 'Boat', 'price' : '1222', 'desc' :'hjhvjhmvbjmh'}
        response = self.client.post('/formelectronics',data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code,302)
        self.assertIn(b'addimage', response.data)
    def test_add_electronics(self):
        response=self.client.get("/formelectronics")
        self.assertEqual(response.status_code,200)

    def test_add_beauty(self):
        data={'name_product' : 'Boat', 'price' : '1222', 'desc' :'hjhvjhmvbjmh'}
        response = self.client.post('/formbeauty',data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code,302)
        self.assertIn(b'addimage', response.data)
    def test_add_beauty(self):
        response=self.client.get("/formbeauty")
        self.assertEqual(response.status_code,200)

    def test_add_fashion(self):
        data={'name_product' : 'Boat', 'price' : '1222', 'desc' :'hjhvjhmvbjmh'}
        response = self.client.post('/formfashion',data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code,302)
        self.assertIn(b'addimage', response.data)
    def test_add_fashion(self):
        response=self.client.get("/formfashion")
        self.assertEqual(response.status_code,200)

    def test_add_home(self):
        data={'name_product' : 'Boat', 'price' : '1222', 'desc' :'hjhvjhmvbjmh'}
        response = self.client.post('/formhome',data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code,302)
        self.assertIn(b'addimage', response.data)  
    def test_add_home(self):
        response=self.client.get("/formhome")
        self.assertEqual(response.status_code,200)
     
    def test_add_sports(self):
        data={'name_product' : 'Boat', 'price' : '1222', 'desc' :'hjhvjhmvbjmh'}
        response = self.client.post('/formsports',data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code,302)
        self.assertIn(b'addimage', response.data) 
    def test_add_sports(self):
        response=self.client.get("/formsports")
        self.assertEqual(response.status_code,200)

    def test_add_books(self):
        data={'name_product' : 'Boat', 'price' : '1222', 'desc' :'hjhvjhmvbjmh'}
        response = self.client.post('/formbooks',data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code,302)
        self.assertIn(b'addimage', response.data) 
    def test_add_books(self):
        response=self.client.get("/formbooks")
        self.assertEqual(response.status_code,200)
    
    def test_logout(self):
        response=self.client.get("/logout")
        self.assertEqual(response.status_code,302)
    def test_team(self):
        response=self.client.get("/team.html")
        self.assertEqual(response.status_code,200)
    def test_home(self):
        response=self.client.get("/home")
        self.assertEqual(response.status_code,200)
    def test_sell(self):
        response=self.client.get("/sellcategory")
        self.assertEqual(response.status_code,200)
    def test_buy(self):
        response=self.client.get("/buycategory")
        self.assertEqual(response.status_code,200)
    def test_index(self):
        response=self.client.get("/")
        self.assertEqual(response.status_code,200)
    def test_returnPolicy(self):
        response=self.client.get("/returnPolicy")
        self.assertEqual(response.status_code,200)
    def test_security(self):
        response=self.client.get("/security")
        self.assertEqual(response.status_code,200)
    def test_contact(self):
        response=self.client.get("/contact")
        self.assertEqual(response.status_code,200)
    def test_product(self):
        response=self.client.get("/product")
        self.assertEqual(response.status_code,200)
    def test_addtocart_productpage(self):
        response=self.client.get("/addedtocart")
        self.assertEqual(response.status_code,302)
    def test_myOrders(self):
        response=self.client.get("/myOrders")
        self.assertEqual(response.status_code,200)
    def test_add_orders(self):
        response=self.client.get("/addorders")
        self.assertEqual(response.status_code,302)
    def test_mySupplies(self):
        response=self.client.get("/mySupplies")
        self.assertEqual(response.status_code,200)
    def test_checkout(self):
        response=self.client.get("/checkout")
        self.assertEqual(response.status_code,200)
    def test_cart(self):
        response=self.client.get("/cart")
        self.assertEqual(response.status_code,200)
    def test_is_cart_empty(self):
        response=self.client.get("/is_Empty")
        self.assertEqual(response.status_code,302)
 
    def test_add_address(self):
        data={'appartment':'kjbk','street':'jhjbh','landmark':"jhhk",'town':"hgvn",'state':"Delhi",'pincode':"245455"}
        response=self.client.post('/add_address',data=data,content_type='multipart/form-data')
        self.assertEqual(response.status_code,302)


    def test_show_personal(self):
        response=self.client.get("/showpersonal")
        self.assertEqual(response.status_code,200)
    def test_add_personal(self):
        response=self.client.get("/showpersonal")
        self.assertEqual(response.status_code,200)
    def test_plus(self):
        response=self.client.get("/cart_plus")
        self.assertEqual(response.status_code,302)
    def test_my_products(self):
        response=self.client.get("/my_products")
        self.assertEqual(response.status_code,200)


if __name__=='__main__':
    unittest.main()