
let optionForm = document.getElementById('new_optionform')
let optionsholder = document.getElementById('optionsHolder')
optionForm.addEventListener('submit',function(event) {
  event.preventDefault()
let optionInput = optionForm.getElementsByTagName('input')[1].value
let div1 = document.createElement('div')
div1.classList = ['col-md-12 col-sm-12 col-md-offset-1']
let div2 = document.createElement('div')
div2.classList = ['form-group row']
let div3 = document.createElement('div')
div3.className = 'col-md-1'
let optiontype = document.getElementById('option_type').value
let inputfieldrep = ""
if (optiontype == "Single" ) {
  inputfieldrep = document.createElement('input')
  inputfieldrep.type = 'radio'
}else {
  inputfieldrep = document.createElement('input')
  inputfieldrep.type = 'checkbox'
}

let inputdata = document.createElement('input')
inputdata.type = 'hidden'
inputdata.name = "options[]"
inputdata.value = optionInput

let label = document.createElement('label')
label.classList = ['col-md-11']
label.appendChild(document.createTextNode(optionInput))
// inputfield.innerHTML =
div3.appendChild(inputfieldrep)
div2.appendChild(div3)
div2.appendChild(label)
div2.appendChild(inputdata)
div1.appendChild(div2)
optionsholder.appendChild(div1)
},false)

let finalOptionsForm = document.getElementById('optionsform')
finalOptionsForm.addEventListener('submit',function(event){
  event.preventDefault()
  let length = finalOptionsForm.getElementsByTagName('input').length
  if (length <= 3 ) {
    alert("No options set For this Question!!")
  }else {
    finalOptionsForm.submit()
  }
},false)
