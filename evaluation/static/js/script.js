$(".meter > span").each(function () {
    $(this)
      .data("origWidth", $(this).width())
      .width(0)
      .animate(
        {
          width: $(this).data("origWidth")
        },
        1100
      );
  });
  
  $(function () {
    var includes = $('[data-include]')
    $.each(includes, function () {
      var file = $(this).data('include') + '.html'
      $(this).load(file)
    })
  })
  


  

  function getRadioValue() {
    var ele1 = document.getElementsByName('remarks1');
    var ele2 = document.getElementsByName('remarks2');
    var ele3 = document.getElementsByName('remarks3');
    var ele4 = document.getElementsByName('remarks4');
    var ele5 = document.getElementsByName('remarks5');
    var ele6 = document.getElementsByName('remarks6');
    var ele7 = document.getElementsByName('remarks7');
    var ele8 = document.getElementsByName('remarks8');
    var ele9 = document.getElementsByName('remarks9');
    var ele10 = document.getElementsByName('remarks10');
    var ele11 = document.getElementsByName('remarks11');
    var ele12 = document.getElementsByName('remarks12');
    var ele13 = document.getElementsByName('remarks13');
    var ele14 = document.getElementsByName('remarks14');
    var ele15 = document.getElementsByName('remarks15');
    var ele16 = document.getElementsByName('remarks16');
    var ele17 = document.getElementsByName('remarks17');
    var ele18 = document.getElementsByName('remarks18');
    var ele19 = document.getElementsByName('remarks19');
    var ele20 = document.getElementsByName('remarks20');
    var ele21 = document.getElementsByName('remarks21');
    var ele22 = document.getElementsByName('remarks22');
    var ele23 = document.getElementsByName('remarks23');
    var ele24 = document.getElementsByName('remarks24');
    var ele25 = document.getElementsByName('remarks25');
    var ele26 = document.getElementsByName('remarks26');
    var ele27 = document.getElementsByName('remarks27');
    var ele28 = document.getElementsByName('remarks28');
    var ele29 = document.getElementsByName('remarks29');
    var ele30 = document.getElementsByName('remarks30');
    var ele31 = document.getElementsByName('remarks31');
    
    
    for(i = 0; i < ele1.length; i++) {
        if(ele1[i].checked)
        document.getElementById("result1").setAttribute("value", ele1[i].value);
    }
    for(i = 0; i < ele2.length; i++) {
      if(ele2[i].checked)
      document.getElementById("result2").setAttribute("value", ele2[i].value);
  }
  for(i = 0; i < ele3.length; i++) {
    if(ele3[i].checked)
    document.getElementById("result3").setAttribute("value", ele3[i].value);
}
for(i = 0; i < ele4.length; i++) {
  if(ele4[i].checked)
  document.getElementById("result4").setAttribute("value", ele4[i].value);
}
for(i = 0; i < ele5.length; i++) {
  if(ele5[i].checked)
  document.getElementById("result5").setAttribute("value", ele5[i].value);
}
for(i = 0; i < ele6.length; i++) {
  if(ele6[i].checked)
  document.getElementById("result6").setAttribute("value", ele6[i].value);
}
for(i = 0; i < ele7.length; i++) {
  if(ele7[i].checked)
  document.getElementById("result7").setAttribute("value", ele7[i].value);
}
for(i = 0; i < ele8.length; i++) {
  if(ele8[i].checked)
  document.getElementById("result8").setAttribute("value", ele8[i].value);
}
for(i = 0; i < ele9.length; i++) {
  if(ele9[i].checked)
  document.getElementById("result9").setAttribute("value", ele9[i].value);
}
for(i = 0; i < ele10.length; i++) {
  if(ele10[i].checked)
  document.getElementById("result10").setAttribute("value", ele10[i].value);
}
for(i = 0; i < ele11.length; i++) {
  if(ele11[i].checked)
  document.getElementById("result11").setAttribute("value", ele11[i].value);
}
for(i = 0; i < ele12.length; i++) {
  if(ele12[i].checked)
  document.getElementById("result12").setAttribute("value", ele12[i].value);
}
for(i = 0; i < ele13.length; i++) {
  if(ele13[i].checked)
  document.getElementById("result13").setAttribute("value", ele13[i].value);
}
for(i = 0; i < ele14.length; i++) {
  if(ele14[i].checked)
  document.getElementById("result14").setAttribute("value", ele14[i].value);
}
for(i = 0; i < ele15.length; i++) {
  if(ele15[i].checked)
  document.getElementById("result15").setAttribute("value", ele15[i].value);
}
for(i = 0; i < ele16.length; i++) {
  if(ele16[i].checked)
  document.getElementById("result16").setAttribute("value", ele16[i].value);
}
for(i = 0; i < ele17.length; i++) {
  if(ele17[i].checked)
  document.getElementById("result17").setAttribute("value", ele17[i].value);
}
for(i = 0; i < ele18.length; i++) {
  if(ele18[i].checked)
  document.getElementById("result18").setAttribute("value", ele18[i].value);
}
for(i = 0; i < ele19.length; i++) {
  if(ele19[i].checked)
  document.getElementById("result19").setAttribute("value", ele19[i].value);
}
for(i = 0; i < ele20.length; i++) {
  if(ele20[i].checked)
  document.getElementById("result20").setAttribute("value", ele20[i].value);
}
for(i = 0; i < ele21.length; i++) {
  if(ele21[i].checked)
  document.getElementById("result21").setAttribute("value", ele21[i].value);
}
for(i = 0; i < ele22.length; i++) {
  if(ele22[i].checked)
  document.getElementById("result22").setAttribute("value", ele22[i].value);
}
for(i = 0; i < ele23.length; i++) {
  if(ele23[i].checked)
  document.getElementById("result23").setAttribute("value", ele23[i].value);
}
for(i = 0; i < ele24.length; i++) {
  if(ele24[i].checked)
  document.getElementById("result24").setAttribute("value", ele24[i].value);
}
for(i = 0; i < ele25.length; i++) {
  if(ele25[i].checked)
  document.getElementById("result25").setAttribute("value", ele25[i].value);
}
for(i = 0; i < ele26.length; i++) {
  if(ele26[i].checked)
  document.getElementById("result26").setAttribute("value", ele26[i].value);
}
for(i = 0; i < ele27.length; i++) {
  if(ele27[i].checked)
  document.getElementById("result27").setAttribute("value", ele27[i].value);
}
for(i = 0; i < ele28.length; i++) {
  if(ele28[i].checked)
  document.getElementById("result28").setAttribute("value", ele28[i].value);
}
for(i = 0; i < ele29.length; i++) {
  if(ele29[i].checked)
  document.getElementById("result29").setAttribute("value", ele29[i].value);
}
for(i = 0; i < ele30.length; i++) {
  if(ele30[i].checked)
  document.getElementById("result30").setAttribute("value", ele30[i].value);
}
for(i = 0; i < ele31.length; i++) {
  if(ele31[i].checked)
  document.getElementById("result31").setAttribute("value", ele31[i].value);
}
comment1 = document.getElementById("comment1").value
comment2 = document.getElementById("comment2").value
comment3 = document.getElementById("comment3").value
comment4 = document.getElementById("comment4").value
document.getElementById("hiddenComment1").setAttribute("value", comment1)
document.getElementById("hiddenComment2").setAttribute("value", comment2)
document.getElementById("hiddenComment3").setAttribute("value", comment3)
document.getElementById("hiddenComment4").setAttribute("value", comment4)
}


function setDefaultPassword(){
  document.getElementById(
    "registerPassword").value = "12345678"
    document.getElementById(
      "registerCPassword").value = "12345678"
  
}


function getFacilitator() {
  var x = document.getElementById("mySelect").value;
  document.getElementById("selected").innerHTML = "Evaluating " + x;
  document.getElementById("selectedFacilitator").setAttribute("value", x);

}