let auth0Client;

const login = async () => {
  // if (!window.location.href.includes("index.html")) {
  //   window.location.href = "index.html";
  // }
  await auth0Client.loginWithRedirect({
    authorizationParams: {
      redirect_uri: window.location.origin + "/index.html"
    }
  });
};

const logout = () => {
  // if (!window.location.href.includes("index.html")) {
  //   window.location.href = "index.html";
  // }

  auth0Client.logout({
    logoutParams: {
      returnTo: window.location.origin + "/index.html"
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
    $(".public-content").hide();

    $("#ipt-user-email").text(user.email);
    // $("#ipt-access-token").text(await auth0Client.getTokenSilently());
    // $("#ipt-user-profile").text(JSON.stringify(await auth0Client.getUser()));


  } else {
    $("#btn-login").show();
    $("#btn-logout").hide();
    $(".gated-content").hide();
    $(".public-content").show();
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
  } else if (query.includes("error=") && query.includes("error_description=")) {
    // if error is "access_denied" and the description contains "verified", display information about how to verify email
    const error = query.split("error=")[1].split("&")[0];
    const error_description = query.split("error_description=")[1].split("&")[0];
    if (error === "access_denied" && error_description.includes("verified")) {
      $("#error-message").text("Please verify your email address before logging in (click the link you received by email).");
    } else {
      $("#error-message").text(error_description);
    }
  }
};

