$(document).ready(function(){
  let $overlay = $("#overlay");
  let $card = $(".card");
  let $cardImg = $(".card-img-top");
  let $btnDanger = $(".btn-danger");
  let $cardTitle = $("card-title");
  let $image = "";
  let imgId = -1;

  $("img").click(function(){
    $overlay.addClass("show");
    $cardImg.attr("src", $(this).attr("src"));
    imgId = $(this).attr("class");
    $image = $(this);
  });

  $overlay.click(function(){
    $overlay.removeClass("show");
  });

  $card.click(function(e){
    e.stopPropagation();
  });

  $btnDanger.click(function(){
    $.post("/deleteimage/" + imgId, function(data){
      if (Object.keys(data)[0] === "success") {
        imgId = -1;
        image = "";
        $overlay.removeClass("show");
        $image.parent().remove();
        $cardTitle.text() = "";
      } else {
        $cardTitle.text() = data[Object.keys(data)[0]];
      }
    });
  });
});
