const usernameField=document.querySelector('#usernameField');
const feedbackArea=document.querySelector('.invalid_feedback');
const emailField=document.querySelector('#emailField');
const emailfeedbackArea=document.querySelector('.emailfeedbackArea');
const usernameSuccessOutput=document.querySelector('.usernameSuccessOutput');
const passwordField=document.querySelector('#passwordField');
const showPasswordToggle=document.querySelector('.showPasswordToggle');
const submitBtn=document.querySelector(".submit-btn")


showPasswordToggle.addEventListener('click',(e) => {
    if(showPasswordToggle.textContent==="SHOW"){
    showPasswordToggle.textContent="HIDE";
    passwordField.setAttribute("type","text");
}else{
    showPasswordToggle.textContent="SHOW";
    passwordField.setAttribute("type","password");

}
});


emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailfeedbackArea.style.display="none";
    
    if (emailVal.length > 0) {
    fetch("/authentication/validate-email",{
        body:JSON.stringify({email: emailVal}),
        method: "POST",
    }).then((res) => res.json())
      .then((data) => {
          if(data.email_error){
              submitBtn.disabled= true;
              emailField.classList.add("is-invalid");
              emailfeedbackArea.style.display="block";
              emailfeedbackArea.innerHTML=`<p>${data.email_error}</p>`;
            }else{
                submitBtn.removeAttribute("disabled");
            }
    });
}
});


usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;

    usernameSuccessOutput.style.display="block";

    usernameSuccessOutput.textContent=`Checking ${usernameVal}`;

    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display="none";
    
    if (usernameVal.length > 0) {
    fetch("/authentication/validate-username",{
        body:JSON.stringify({username: usernameVal}),
        method: "POST",
    }).then((res) => res.json())
      .then((data) => {
        usernameSuccessOutput.style.display='none';
          if(data.username_error){
              submitBtn.disabled=true;
              usernameField.classList.add("is-invalid");
              feedbackArea.style.display="block";
              feedbackArea.innerHTML=`<p>${data.username_error}</p>`;
            }else{
                submitBtn.removeAttribute("disabled");
            }
    });
}
});