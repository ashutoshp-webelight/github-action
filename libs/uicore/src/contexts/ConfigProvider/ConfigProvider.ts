import { createContext, useContext } from "react";
import { SIZES } from "@uicore/constants";
import type { ColorLevel, TypeAttributes } from "./types";

type Config = {
  themeColor: string;
  mode: "light" | "dark";
  locale: string;
  primaryColorLevel: ColorLevel;
  cardBordered: boolean;
  controlSize: TypeAttributes.ControlSize;
  navMode: TypeAttributes.MenuVariant;
  direction: TypeAttributes.Direction;
};

export const defaultConfig = {
  themeColor: "indigo",
  direction: "ltr",
  mode: "light",
  locale: "en",
  primaryColorLevel: 600,
  cardBordered: false,
  controlSize: SIZES.MD,
  navMode: "light",
} as const;

export const ConfigContext = createContext<Config>(defaultConfig);

export const ConfigProvider = ConfigContext.Provider;

export const ConfigConsumer = ConfigContext.Consumer;

export function useConfig() {
  return useContext(ConfigContext);
}
