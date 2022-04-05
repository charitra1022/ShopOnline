function scrollDiv() {

    var productList = document.getElementsByClassName("product-list");

    var checkBoxes = document.getElementsByClassName("autoscroll-checkbox");

    for (let i = 0; i < productList.length; i++) {

      if(checkBoxes[i].checked===false){
        continue;
      }
      const scroll_width = productList[i].scrollWidth;
      const off_width = productList[i].offsetWidth;
      const scrollPos = productList[i].scrollLeft;
      const scrollBy = 10;

      // var debug_msg = `Width:${scroll_width} offset:${off_width} pos:${scrollPos}`;
      // console.log(debug_msg);

      productList[i].scrollLeft += scrollBy;
      if (scrollPos === scroll_width - off_width) {
        productList[i].scrollLeft = 0;
      }
    }
  
}

window.onload = () => {
  setInterval(scrollDiv, 500);
};
