$(document).ready(function(){
  $('#skillsTable').DataTable();
  let $deleteSkill = $(".deleteSkill");

  $deleteSkill.click(function() {
    let id = $(this).closest("tr").attr('id');
    $.post(`/api/deleteskill?id=${id}`, function(data) {
      console.log(data);
    });
    $(this).closest("tr").remove();
  });
});
