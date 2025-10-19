export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405 });
    }

    const { company_name, items } = await request.json();

    const response = await fetch(
      "https://api.github.com/repos/mohitmsingh/utility/dispatches",
      {
        method: "POST",
        headers: {
          "Authorization": `token ${env.GITHUB_PAT}`,
          "Accept": "application/vnd.github+json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          event_type: "generate-invoice",
          client_payload: { company_name, items }
        })
      }
    );

    if (response.ok) return new Response(JSON.stringify({ success: true }));
    else return new Response(await response.text(), { status: 500 });
  }
};
