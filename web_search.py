from ddgs import DDGS


def search_web(query):

    results_text = ""

    try:

        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=5
            )

            for result in results:

                title = result.get(
                    "title",
                    ""
                )

                body = result.get(
                    "body",
                    ""
                )

                href = result.get(
                    "href",
                    ""
                )

                results_text += (
                    f"Title: {title}\n"
                    f"Info: {body}\n"
                    f"Link: {href}\n\n"
                )

    except Exception as error:

        return f"Web search failed: {error}"

    if not results_text:

        return "No web results found."

    return results_text