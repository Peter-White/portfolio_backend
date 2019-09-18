$(document).ready(function(){
  let table = $('#skillsTable').DataTable();

  let deleter = $("button.deleter");

  deleter.click(function() {
    if($(".selected").length > 0) {
      deleteSkills($(".selected").length);
    } else {
      alert("No skills selected");
    }
  });

  $('#skillsTable tbody').on( 'click', 'tr', function () {
    if($(this).hasClass('selected')) {
      $(this).removeClass('selected');
    } else {
      $(this).addClass('selected');
    }
  });

  let deleteSkills = function(length) {
    for(let i = 0; i < length; i++) {
      let selected = $('.selected');
      let selected_id = selected.attr('id');

      if(confirm("Are you sure you want to delete this skill")) {
        $.post(`/api/deleteskill?id=${selected_id}`, function(data) {
          if(Object.keys(data)[0] === "success") {
            table.row(selected).remove().draw( false );
          } else {
            alert("FAIL");
            return;
          }
        });
      }
    }
  };

});
