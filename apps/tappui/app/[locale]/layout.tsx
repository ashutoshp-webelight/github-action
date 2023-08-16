"use client";

import "./global.css";
import { NextIntlClientProvider } from "next-intl";
import { notFound } from "next/navigation";
import { ConfigProvider, defaultConfig } from "@uicore/contexts";

type Params = {
  locale: string;
};

export function generateStaticParams() {
  return [{ locale: "en" }, { locale: "de" }];
}

const RootLayout = async ({
  children,
  params: { locale },
}: {
  children: React.ReactNode;
  params: Params;
}) => {
  let messages;
  try {
    messages = (await import(`../../messages/${locale}.json`)).default;
  } catch (error) {
    notFound();
  }

  return (
    <html lang={locale}>
      <body>
        <NextIntlClientProvider locale={locale} messages={messages}>
          <ConfigProvider value={defaultConfig}>{children}</ConfigProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  );
};

export default RootLayout;
