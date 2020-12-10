function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
 
 const favButtons = document.querySelectorAll('.custom-card__bottom i')

      favButtons.forEach(favButton => {
        favButton.addEventListener('click', (e) => {
          let id = e.target.parentElement.dataset.id;
          const token = getCookie('csrftoken');
      
          fetch(`/note/fav/`, {
            method: 'POST',
            body: JSON.stringify({
              'id': id
            }),
            headers: {
              'Accept': 'application/json; charset=UTF-8',
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': token
            },
            credentials: 'same-origin'
          }).then(res => res.json())
          .then(data => {
            if (data.status === 200) {
             e.target.parentElement.classList.toggle('fav')
            } 
          })
          .catch(err => console.log(err))
        })
      })