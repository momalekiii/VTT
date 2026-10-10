// ==UserScript==
// @name         VTT — Online Video Subtitles (Persian & English)
// @namespace    https://github.com/momalekiii/VTT
// @version      2.0.2
// @description  Minimal online subtitle overlay for YouTube and any video playing in Chrome — built for Persian (FA) and English (EN).
// @author       @momalekiii
// @homepageURL  https://github.com/momalekiii/VTT
// @downloadURL  https://github.com/momalekiii/VTT/raw/main/vtt-subtitles.user.js
// @updateURL    https://github.com/momalekiii/VTT/raw/main/vtt-subtitles.user.js
// @match        http://*/*
// @match        https://*/*
// @run-at       document-idle
// @grant        GM_xmlhttpRequest
// @connect      translate.googleapis.com
// @connect      clients5.google.com
// @connect      api.mymemory.translated.net
// ==/UserScript==

(function () {
  "use strict";

  if (window.__VTT_USERSCRIPT_LOADED__ || window.__VTT_MINIMAL_LOADED__) return;
  window.__VTT_USERSCRIPT_LOADED__ = true;

  var styleEl = document.createElement("style");
  styleEl.textContent = [
    "html.vtt-hide-native-cc .ytp-caption-window-container, html.vtt-hide-native-cc .vjs-text-track-display, html.vtt-hide-native-cc .jw-captions, html.vtt-hide-native-cc .plyr__captions { opacity: 0 !important; pointer-events: none !important; }",
    ".vtt-minimal-wrap { position: fixed; z-index: 2147483647; left: 50%; bottom: 68px; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; max-width: min(86vw, 760px); width: max-content; pointer-events: none; transition: opacity 0.14s ease, transform 0.14s ease; font-family: 'Vazirmatn', 'Inter', 'Tahoma', system-ui, -apple-system, sans-serif; }",
    ".vtt-minimal-wrap.vtt-hidden { opacity: 0 !important; transform: translateX(-50%) translateY(4px); }",
    ".vtt-minimal-box { pointer-events: auto; display: flex; flex-direction: column; align-items: center; gap: 3px; padding: 7px 16px; border-radius: 10px; background: rgba(8, 10, 16, 0.82); border: 1px solid rgba(255, 255, 255, 0.11); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.55); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); text-align: center; max-width: 100%; }",
    ".vtt-minimal-line-main { color: #f4f6fb; font-weight: 600; line-height: 1.5; unicode-bidi: plaintext; text-shadow: 0 1px 4px rgba(0, 0, 0, 0.88); word-break: break-word; font-size: 19px; }",
    ".vtt-minimal-line-sub { color: rgba(94, 234, 212, 0.90); font-size: 12.5px; font-weight: 400; line-height: 1.36; unicode-bidi: plaintext; word-break: break-word; }",
    ".vtt-video-chip { position: fixed; z-index: 2147483647; top: 66px; right: 14px; left: auto; display: inline-flex; align-items: center; gap: 2px; padding: 2px 6px; border-radius: 999px; background: rgba(8, 10, 16, 0.72); border: 1px solid rgba(255, 255, 255, 0.12); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); color: #f2f4fa; font-family: 'Inter', 'Vazirmatn', system-ui, sans-serif; font-size: 9.5px; opacity: 0.14; transform: scale(0.94); transform-origin: top right; transition: opacity 0.2s ease, transform 0.2s ease, border-color 0.2s ease, background 0.2s ease; user-select: none; }",
    ".vtt-video-chip:hover { opacity: 1; transform: scale(1); background: rgba(8, 10, 16, 0.90); border-color: rgba(94, 234, 212, 0.45); }",
    ".vtt-video-chip.vtt-chip-hidden { display: none !important; }",
    ".vtt-chip-dot { width: 5px; height: 5px; border-radius: 50%; background: #5eead4; margin-right: 2px; }",
    ".vtt-chip-dot.vtt-off { background: rgba(255, 255, 255, 0.28); }",
    ".vtt-chip-btn { appearance: none; border: none; background: transparent; color: rgba(242, 244, 250, 0.72); font-size: 9.5px; font-weight: 600; padding: 1px 4px; border-radius: 999px; cursor: pointer; line-height: 1.3; }",
    ".vtt-chip-btn.active { background: rgba(94, 234, 212, 0.18); color: #5eead4; }",
  ].join("\n");
  (document.head || document.documentElement).appendChild(styleEl);

  var cache = new Map();
  var state = {
    enabled: true,
    targetLang: "fa",
    activeVideo: null,
    lastRawCaption: "",
    shownDomPrefix: "",
    pendingDomCaption: "",
    holdUntilMs: 0,
    holdFlushTimer: null,
    wrapEl: null,
    mainLineEl: null,
    subLineEl: null,
    chipEl: null,
    hideTimer: null,
    debounceTimer: null,
  };

  function isRTL(str) {
    return /[\u0600-\u06FF]/.test(str || "");
  }

  function normalizeFa(text) {
    return String(text || "")
      .replace(/[\u064A\u0649]/g, "\u06CC")
      .replace(/\u0643/g, "\u06A9")
      .replace(/\s+/g, " ")
      .trim();
  }

  function translateText(text, lang, cb) {
    var clean = (text || "").trim();
    if (!clean) return cb("");
    var key = lang + "::" + clean;
    if (cache.has(key)) return cb(cache.get(key));

    var url =
      "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" +
      encodeURIComponent(lang) +
      "&dt=t&q=" +
      encodeURIComponent(clean);

    if (typeof GM_xmlhttpRequest === "function") {
      GM_xmlhttpRequest({
        method: "GET",
        url: url,
        onload: function (res) {
          try {
            var data = JSON.parse(res.responseText);
            var out = (data[0] || [])
              .map(function (x) {
                return Array.isArray(x) ? x[0] : "";
              })
              .join("")
              .trim();
            if (lang === "fa") out = normalizeFa(out);
            cache.set(key, out || clean);
            cb(out || clean);
          } catch (_e) {
            cb(clean);
          }
        },
        onerror: function () {
          cb(clean);
        },
      });
    } else {
      fetch(url)
        .then(function (r) {
          return r.json();
        })
        .then(function (data) {
          var out = (data[0] || [])
            .map(function (x) {
              return Array.isArray(x) ? x[0] : "";
            })
            .join("")
            .trim();
          if (lang === "fa") out = normalizeFa(out);
          cache.set(key, out || clean);
          cb(out || clean);
        })
        .catch(function () {
          cb(clean);
        });
    }
  }

  function ensureUI() {
    var host = document.fullscreenElement || document.body;
    if (!host) return;
    if (!state.wrapEl) {
      var wrap = document.createElement("div");
      wrap.className = "vtt-minimal-wrap vtt-hidden";
      var box = document.createElement("div");
      box.className = "vtt-minimal-box";
      var main = document.createElement("div");
      main.className = "vtt-minimal-line-main";
      var sub = document.createElement("div");
      sub.className = "vtt-minimal-line-sub";
      sub.style.display = "none";
      box.appendChild(main);
      box.appendChild(sub);
      wrap.appendChild(box);
      host.appendChild(wrap);
      state.wrapEl = wrap;
      state.mainLineEl = main;
      state.subLineEl = sub;
    }
    if (!state.chipEl) {
      var chip = document.createElement("div");
      chip.className = "vtt-video-chip vtt-chip-hidden";
      chip.innerHTML =
        '<span class="vtt-chip-dot" id="vtt-chip-dot"></span>' +
        '<button type="button" class="vtt-chip-btn active" data-lang="fa">FA</button>' +
        '<button type="button" class="vtt-chip-btn" data-lang="en">EN</button>' +
        '<button type="button" class="vtt-chip-btn" data-lang="both">FA+EN</button>';
      host.appendChild(chip);
      state.chipEl = chip;

      chip.querySelectorAll("[data-lang]").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
          e.stopPropagation();
          var l = btn.getAttribute("data-lang");
          if (state.enabled && state.targetLang === l) {
            state.enabled = false;
          } else {
            state.targetLang = l;
            state.enabled = true;
          }
          state.holdUntilMs = 0;
          document.documentElement.classList.toggle(
            "vtt-hide-native-cc",
            state.enabled
          );
          chip.querySelectorAll("[data-lang]").forEach(function (b) {
            b.classList.toggle(
              "active",
              state.enabled && b.getAttribute("data-lang") === state.targetLang
            );
          });
          if (!state.enabled) state.wrapEl.classList.add("vtt-hidden");
          else if (state.lastRawCaption) renderCaption(state.lastRawCaption, true);
        });
      });
    }
  }

  function positionOverlay(video) {
    ensureUI();
    if (!video || !state.wrapEl || !state.chipEl) return;
    var rect = video.getBoundingClientRect();
    if (rect.width < 120 || rect.height < 80) return;
    var visibleBottom = Math.min(window.innerHeight, rect.bottom);
    state.wrapEl.style.left = Math.round(rect.left + rect.width / 2) + "px";
    state.wrapEl.style.bottom =
      Math.round(
        Math.max(24, window.innerHeight - visibleBottom + rect.height * 0.11)
      ) + "px";
    state.chipEl.style.top = Math.round(Math.max(60, rect.top + 8)) + "px";
    state.chipEl.style.right =
      Math.round(Math.max(8, window.innerWidth - rect.right + 8)) + "px";
    state.chipEl.classList.remove("vtt-chip-hidden");
  }

  function renderCaption(rawText, immediate) {
    var clean = (rawText || "").replace(/\s+/g, " ").trim();
    if (!clean) return;
    var now = Date.now();
    if (!immediate && now < state.holdUntilMs) {
      state.pendingDomCaption = clean;
      if (!state.holdFlushTimer) {
        state.holdFlushTimer = setTimeout(function () {
          state.holdFlushTimer = null;
          if (state.pendingDomCaption) {
            var next = state.pendingDomCaption;
            state.pendingDomCaption = "";
            renderCaption(next, true);
          }
        }, Math.max(120, state.holdUntilMs - now));
      }
      return;
    }

    var run = function () {
      state.lastRawCaption = clean;
      document.documentElement.classList.add("vtt-hide-native-cc");
      var target = state.targetLang === "both" ? "fa" : state.targetLang;
      translateText(clean, target, function (mainTxt) {
        if (!state.enabled || !mainTxt) return;
        var hold = Math.max(2800, Math.min(5200, 1900 + mainTxt.length * 52));
        state.holdUntilMs = Date.now() + hold;
        if (state.activeVideo) positionOverlay(state.activeVideo);
        state.mainLineEl.textContent = mainTxt;
        state.mainLineEl.dir = isRTL(mainTxt) ? "rtl" : "ltr";
        if (state.targetLang === "both" && clean !== mainTxt) {
          state.subLineEl.textContent = clean;
          state.subLineEl.style.display = "block";
        } else {
          state.subLineEl.style.display = "none";
        }
        state.wrapEl.classList.remove("vtt-hidden");
      });
    };

    if (immediate) return run();
    if (state.debounceTimer) clearTimeout(state.debounceTimer);
    state.debounceTimer = setTimeout(run, 650);
  }

  setInterval(function () {
    var vids = Array.from(document.querySelectorAll("video"));
    if (vids.length === 0) return;
    var v = vids[0];
    state.activeVideo = v;
    positionOverlay(v);
    if (!state.enabled) return;

    var ccBtn = document.querySelector(".ytp-subtitles-button");
    if (ccBtn && ccBtn.getAttribute("aria-pressed") === "false") {
      document.documentElement.classList.add("vtt-hide-native-cc");
      try {
        ccBtn.click();
      } catch (_e) {}
    }

    var nodes = document.querySelectorAll(
      ".ytp-caption-segment, .vjs-text-track-cue, .plyr__caption"
    );
    if (nodes.length > 0) {
      var txt = Array.from(nodes)
        .map(function (n) {
          return (n.textContent || "").trim();
        })
        .filter(Boolean)
        .join(" ");
      if (txt && txt !== state.lastRawCaption) {
        renderCaption(txt, false);
      }
    }
  }, 500);
})();
