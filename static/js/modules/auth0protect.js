let auth0Client;

const login = async () => {
  if (!window.location.href.includes("index.html")) {
    window.location.href = "index.html";
  }
  await auth0Client.loginWithRedirect({
    authorizationParams: {
      redirect_uri: window.location.href
    }
  });
};

const logout = () => {
  if (!window.location.href.includes("index.html")) {
    window.location.href = "index.html";
  }

  auth0Client.logout({
    logoutParams: {
      returnTo: window.location.href
    }
  });
};


const configureClient = async () => {
  auth0Client = await auth0.createAuth0Client({
    domain: auth0_domain,
    clientId: auth0_client_id
  });
};

const updateUI = async () => {
  console.log(auth0Client, "--- auth0Client");
  const is_auth = await auth0Client.isAuthenticated();
  console.log(is_auth, "--- is_auth");

  if (is_auth) {
    document.body.style.display = null;

    const user = await auth0Client.getUser();
    $("#btn-login").hide();
    $("#btn-logout").show();

    $(".gated-content").show();
    $("#ipt-access-token").text(await auth0Client.getTokenSilently());
    $("#ipt-user-profile").text(JSON.stringify(await auth0Client.getUser()));


  } else {
    $("#btn-login").show();
    $("#btn-logout").hide();
    $(".gated-content").hide();
  }
};


window.onload = async () => {
  console.log("window.onload");
  await configureClient();

  updateUI();

  // NEW - check for the code and state parameters
  const query = window.location.search;
  if (query.includes("code=") && query.includes("state=")) {

    // Process the login state
    console.log("processing login state");
    await auth0Client.handleRedirectCallback();
    console.log("redirect callback handled");
    updateUI();

    // Use replaceState to redirect the user away and remove the querystring parameters
    window.history.replaceState({}, document.title, "/");
  }
};

