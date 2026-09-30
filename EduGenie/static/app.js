/* EduGenie frontend: progressive enhancement only.
   Every form posts to /process and works without JS. This file upgrades them
   to fetch() so each answer renders in its own panel without a page reload. */
(function () {
    "use strict";

    /* ---------- Markdown -> HTML ----------
       Escapes first, then formats, so model output can never inject HTML. */
    function escapeHtml(s) {
        return s.replace(/&/g, "&amp;").replace(/</g, "&lt;")
                .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }

    function inline(s) {
        return s
            .replace(/`([^`]+)`/g, "<code>$1</code>")
            .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
            .replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>");
    }

    function renderMarkdown(src) {
        var lines = String(src).replace(/\r\n/g, "\n").split("\n");
        var html = [], listType = null, inCode = false, codeBuf = [];

        function closeList() {
            if (listType) { html.push("</" + listType + ">"); listType = null; }
        }

        for (var i = 0; i < lines.length; i++) {
            var line = lines[i];

            if (/^```/.test(line)) {
                if (inCode) {
                    html.push("<pre><code>" + escapeHtml(codeBuf.join("\n")) + "</code></pre>");
                    codeBuf = []; inCode = false;
                } else {
                    closeList(); inCode = true;
                }
                continue;
            }
            if (inCode) { codeBuf.push(line); continue; }
            if (!line.trim()) { closeList(); continue; }

            var heading = line.match(/^(#{1,4})\s+(.*)$/);
            if (heading) {
                closeList();
                var lvl = heading[1].length + 1; // output h1 -> panel h2
                html.push("<h" + lvl + ">" + inline(escapeHtml(heading[2])) + "</h" + lvl + ">");
                continue;
            }

            var quote = line.match(/^>\s?(.*)$/);
            if (quote) {
                closeList();
                html.push("<blockquote>" + inline(escapeHtml(quote[1])) + "</blockquote>");
                continue;
            }

            var ul = line.match(/^\s*[-*+]\s+(.*)$/);
            var ol = line.match(/^\s*\d+[.)]\s+(.*)$/);
            if (ul || ol) {
                var want = ul ? "ul" : "ol";
                if (listType !== want) { closeList(); html.push("<" + want + ">"); listType = want; }
                html.push("<li>" + inline(escapeHtml((ul || ol)[1])) + "</li>");
                continue;
            }

            closeList();
            html.push("<p>" + inline(escapeHtml(line)) + "</p>");
        }

        closeList();
        if (inCode) html.push("<pre><code>" + escapeHtml(codeBuf.join("\n")) + "</code></pre>");
        return html.join("");
    }

    /* ---------- Quiz rendering ---------- */
    function renderQuiz(quiz) {
        if (!Array.isArray(quiz) || !quiz.length) {
            return '<p class="error">No quiz could be generated. Please try again.</p>';
        }
        return quiz.map(function (q, i) {
            var opts = (q.options || []).map(function (o) {
                return "<li>" + escapeHtml(String(o)) + "</li>";
            }).join("");
            return '<div class="quiz-item">' +
                '<p class="quiz-q"><span class="quiz-num">' + (i + 1) + "</span>" +
                escapeHtml(String(q.question || "")) + "</p>" +
                '<ul class="quiz-options">' + opts + "</ul>" +
                '<button type="button" class="btn-reveal">Show correct answer</button>' +
                '<p class="answer" hidden><em>Correct answer: ' +
                escapeHtml(String(q.correct_answer || "")) + "</em></p>" +
                "</div>";
        }).join("");
    }

    /* ---------- Toast ---------- */
    var toast = document.getElementById("toast");
    function toastMsg(msg) {
        if (!toast) return;
        toast.textContent = msg;
        toast.classList.add("show");
        setTimeout(function () { toast.classList.remove("show"); }, 1800);
    }

    /* ---------- Wire up each form ---------- */
    Array.prototype.forEach.call(document.querySelectorAll("form[data-api]"), function (form) {
        var panel = form.nextElementSibling;          // the .output div
        var button = form.querySelector("button[type=submit]");
        var field = form.querySelector("input[name=user_input]");

        form.addEventListener("submit", function (e) {
            e.preventDefault();                        // no page reload
            var value = (field.value || "").trim();
            if (!value) return;

            var original = button.textContent;
            button.disabled = true;
            button.textContent = "Generating…";
            panel.classList.add("loading");
            panel.innerHTML =
                '<div class="spinner-lg" aria-hidden="true"></div>' +
                '<p class="loading-text">Generating with Gemini…</p>' +
                '<p class="loading-sub">This usually takes 5–20 seconds.</p>';

            // Each endpoint expects its own field name.
            var params = { "user_input": value };
            if (field.id === "question") params = { question: value };
            else if (field.id === "topic") params = { topic: value };
            else if (field.id === "learnTopic") params = { topic: value };
            else if (field.id === "summaryText") params = { passage: value };
            else if (field.id === "quizText") params = { passage: value };

            fetch(form.dataset.api, {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams(params)
            })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (form.dataset.key === "quiz") {
                        panel.innerHTML = renderQuiz(data.quiz);
                    } else {
                        panel.innerHTML = '<div class="markdown-output">' +
                            renderMarkdown(data.result || "") + "</div>";
                    }
                })
                .catch(function () {
                    panel.innerHTML = '<p class="error">Could not reach the server. ' +
                        "Is EduGenie still running? Please try again.</p>";
                })
                .then(function () {
                    button.disabled = false;
                    button.textContent = original;
                    panel.classList.remove("loading");
                });
        });
    });

    /* ---------- Quiz answer reveal (delegated) ---------- */
    document.addEventListener("click", function (e) {
        var btn = e.target.closest ? e.target.closest(".btn-reveal") : null;
        if (!btn) return;
        var answer = btn.parentElement.querySelector(".answer");
        if (!answer) return;
        var showing = !answer.hidden;
        answer.hidden = showing;
        btn.textContent = showing ? "Show correct answer" : "Hide answer";
    });



    /* ---------- Dark mode (remembered) ---------- */
    var toggle = document.getElementById("themeToggle");
    var stored = null;
    try { stored = localStorage.getItem("edugenie-theme"); } catch (e) { /* private mode */ }

    function setTheme(mode) {
        document.documentElement.setAttribute("data-theme", mode);
        if (toggle && toggle.firstElementChild) {
            toggle.firstElementChild.textContent = mode === "dark" ? "☀" : "☾";
        }
    }

    var prefersDark = window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches;
    setTheme(stored || (prefersDark ? "dark" : "light"));

    if (toggle) {
        toggle.addEventListener("click", function () {
            var next = document.documentElement.getAttribute("data-theme") === "dark"
                ? "light" : "dark";
            setTheme(next);
            try { localStorage.setItem("edugenie-theme", next); } catch (e) { /* ignore */ }
        });
    }

    /* ---------- Ctrl/Cmd+Enter submits ---------- */
    Array.prototype.forEach.call(
        document.querySelectorAll("input[name=user_input]"),
        function (input) {
            input.addEventListener("keydown", function (e) {
                if ((e.ctrlKey || e.metaKey) && e.key === "Enter" && input.form) {
                    input.form.requestSubmit();
                }
            });
        }
    );
})();
