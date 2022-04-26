$('.plus-cart').click(function () {
  var id = $(this).attr("pid");
  var quantity_el = this.parentNode.children[2];
  var ship_amt_el = document.getElementById('shipping-amount');
  var total_amt_el = document.getElementById('total-amount');
  var final_amt_el = document.getElementById('final-amount');

  $.ajax({
    type: "GET",
    url: "/pluscartitem",
    data: {
      product_id: id,
    },
    success: function (data) {
      console.log(data);
      quantity_el.innerText = data.quantity;
      ship_amt_el.innerText = data.shippingamount;
      total_amt_el.innerText = data.totalamount;
      final_amt_el.innerText = data.finalamount;
    }
  })
})

$('.minus-cart').click(function () {
  var id = $(this).attr("pid");
  var quantity_el = this.parentNode.children[2];
  var ship_amt_el = document.getElementById('shipping-amount');
  var total_amt_el = document.getElementById('total-amount');
  var final_amt_el = document.getElementById('final-amount');

  $.ajax({
    type: "GET",
    url: "/minuscartitem",
    data: {
      product_id: id,
    },
    success: function (data) {
      console.log(data);
      quantity_el.innerText = data.quantity;
      ship_amt_el.innerText = data.shippingamount;
      total_amt_el.innerText = data.totalamount;
      final_amt_el.innerText = data.finalamount;
    }
  })
})

$('.delete-cart').click(function () {
  var id = $(this).attr("pid");
  console.log(`trash ${id}`);
})