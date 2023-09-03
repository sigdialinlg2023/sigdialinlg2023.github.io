

function sessIDtoLink(match, sessionLinks){

  var sessLink = match.substring(3, match.length - 3);
  if (sessLink.includes('%')) {
      sessLink = decodeURIComponent(sessLink);
  }

  if (sessLink in sessionLinks.rooms2zoom) {
    return sessionLinks.rooms2zoom[sessLink];
  }
  else if (sessLink in sessionLinks.session2discord) {
    return sessionLinks.session2discord[sessLink];
  }
  else if (sessLink in sessionLinks.posters2discords) {
    return sessionLinks.posters2discords[sessLink];
  }
  return match; // do nothing if not found
}

async function updateLinks(){

  // Get all hyperlinks on the page
  const links = document.querySelectorAll('a');
  const searchRegex = /###[a-zA-Z0-9% ]+###/g;
  const sessionLinks = await API.getSessionLinks();

  // Loop through each link
  links.forEach(link => {
    // Replace in the URL
    link.href = link.href.replace(searchRegex, match => {
      return sessIDtoLink(match, sessionLinks);
    });

    // Replace in the link text
    link.textContent = link.textContent.replace(searchRegex, match => {
      return sessIDtoLink(match, sessionLinks);
    });
  });
}
