"use client";

import { useTranslations } from "next-intl";
import { InputField } from "@uicore/components";
import { InputVariant } from "@uicore/constants";

const Home = () => {
  const t = useTranslations("Index");

  return (
    <div
      style={{
        alignItems: "center",
        display: "flex",
        height: "100vh",
      }}
    >
      <h1 className="uppercase">{t("welcome")}</h1>
      <InputField
        label={"Name"}
        placeholder="Enter your email"
        variant={InputVariant.open}
      />
    </div>
  );
};

export default Home;
