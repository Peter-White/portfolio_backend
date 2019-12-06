$(document).ready(function(){
  let url = window.location.href.split("/");

  let $overlay = $("#overlay");
  let $card = $(".card");
  let $cardImg = $(".card-img-top");
  let $btnDanger = $(".btn-danger");
  let $cardTitle = $("card-title");
  let $dropdownItem = $("button.dropdown-item");
  let $skill = $("li#skill");
  let projectId = parseInt(url[url.length - 1]);
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

  $(document.body).on('click', 'li#skill', function() {
    let skill = $(this);
    if(confirm("Are you sure you want to remove this skill from this project?")) {
      $.post("/deleteprojectskill?skill=" + $(this).attr("class") + "&project=" + projectId, function(data){
        if (Object.keys(data)[0] === "success") {
          skill.remove();
        } else {
          alert(data[Object.keys(data)[0]]);
        }
      });
    }
  });

  $dropdownItem.click(function() {
    $.post("/addprojectskill?skill=" + $(this).attr("id") + "&project=" + projectId, function(data){
      if (Object.keys(data)[0] === "success") {
        let $categoryList = $("ul." + data[Object.keys(data)[0]]["category"]);
        $categoryList.append('<li id="skill" class=' + data[Object.keys(data)[0]]["id"] + '>' + data[Object.keys(data)[0]]["title"] + '<span class="deleteX">✘</span></li>')
        $(this).remove();
        $skill = $("li#skill");
        console.log($skill);
      } else {
        alert(data[Object.keys(data)[0]]);
      }
    });
  });
});
