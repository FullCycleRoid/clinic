(function(){
 if (window.myBookmarklet !== undefined){
  console.log('launch Bookmarklet')
 myBookmarklet();
 }
 else {
 console.log('Create Bookmarklet')
 document.body.appendChild(
 document.createElement('script')
 ).src='expleo.serveousercontent.com/static/js/bookmarklet.js?r=' +
 Math.floor(Math.random()*99999999999999999999);
 }
})();