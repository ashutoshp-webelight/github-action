import { InputVariant } from "@uicore/constants";
import { Input, InputProps } from "../Input";
import "./style.css";

interface InputFieldProps extends InputProps {
  label?: string;
  required?: boolean;
  classes?: {
    container: string;
    label: string;
    input: string;
  };
  variant?: InputVariant;
  error?: {
    type: string;
    message: string;
  };
}

export const InputField = ({
  label = "",
  value = "",
  onChange,
  placeholder = "input",
  type,
  required = false,
  classes,
  variant = InputVariant.close,
  error,
  ...inputProps
}: InputFieldProps) => {
  const getVariantClasses = () => {
    switch (variant) {
      case InputVariant.open: {
        return "open_input";
      }
      case InputVariant.close: {
        return "close_input";
      }
    }
  };

  return (
    <div className={`inputfield_container ${classes?.container}`}>
      <label className={`input_label ${classes?.label}`}>
        {label} {required && "*"}
      </label>
      <Input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className={`inputfield ${getVariantClasses()} ${classes?.input}`}
        required={required}
        {...inputProps}
      />
      {Boolean(error) && <small>{error?.message}</small>}
    </div>
  );
};
