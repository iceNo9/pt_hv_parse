import { defineConfig } from "vitepress";
import { withPwa } from "@vite-pwa/vitepress";

// https://vitepress.dev/reference/site-config
export default withPwa(
  defineConfig({
    title: "pt_hv_parse",
    description: "解析高压参数",
    themeConfig: {
      // https://vitepress.dev/reference/default-theme-config
      logo: "/logo.png",
      nav: [
        { text: "Home", link: "/" },
        { text: "Guide", link: "/guide/" },
        { text: "API", link: "/api/" },
        {
          text: "GitHub",
          link: "https://github.com/iceNo9/pt_hv_parse",
        },
      ],
      sidebar: [
        {
          text: "Introduction",
          items: [
            { text: "Getting Started", link: "/guide/" },
            { text: "Installation", link: "/guide/installation" },
          ],
        },
        {
          text: "API Reference",
          items: [
            { text: "Overview", link: "/api/" },
            { text: "Examples", link: "/api/examples" },
          ],
        },
      ],
      socialLinks: [
        {
          icon: "github",
          link: "https://github.com/iceNo9/pt_hv_parse",
        },
      ],
      footer: {
        message: "Released under the MIT License.",
        copyright:
          'Copyright © 2025 hupo',
      },
    },
    pwa: {
      manifest: {
        name: "pt_hv_parse",
        short_name: "pt_hv_parse",
        theme_color: "#2b2a27",
        background_color: "#ffffff",
        display: "standalone",
        orientation: "portrait",
        scope: "/",
        start_url: "/",
        icons: [
          {
            src: "/logo.png",
            sizes: "192x192",
            type: "image/png",
            purpose: "maskable any",
          },
        ],
      },
    },
  })
);
