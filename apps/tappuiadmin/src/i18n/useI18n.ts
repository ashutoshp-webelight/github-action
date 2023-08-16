import { useTranslation } from "react-i18next";

export const useI18n: typeof useTranslation = (...args) => {
  const result = useTranslation(...args);

  return {
    ...result,
  };
};
