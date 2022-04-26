def cart_count(request):
  # Adds a context to all templates for cart items counter for badge update
  counter = 0
  from app.models import Cart
  try:
    counter = Cart.objects.filter(user=request.user).count()
    print(counter)
  except:
    counter = 0
  return {'cart_counter': counter}
