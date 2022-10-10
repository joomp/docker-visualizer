/**
 * Returns a new string created from str with the first letter capitalized
 *
 * @param {string} str Target string
 * @returns {string} Capitalized string
 */
export const capitalize = (str) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

/**
 * Checks if the date is a valid date.
 *
 * @param {Date} date target date
 * @returns {boolean} results
 */
const isValidDate = (date) => {
  return date instanceof Date && !isNaN(date);
};

/**
 * Converts the date to a string. The string contains both the date and the time.
 * Returns null for invalid dates.
 *
 * @param {Date|string|number} date A date object, or a value that can create date object. Numbers are treated as UNIX timestamps.
 * @returns {string|null} The result
 */
export const dateToString = (date) => {
  if (Number.isInteger(date)) date = date * 1000;
  const d = new Date(date);
  if (isValidDate(d))
    return `${d.toLocaleTimeString()},  ${d.toLocaleDateString()}`;
  return null;
};

/**
 * Returns the string in short id format.
 *
 * @param {string} str - target string
 * @returns {string} short id
 */
export const shortId = (str) => {
  const len = 13;
  return str.slice(0, len) + '...';
};

/**
 * Returns the string in short name format.
 *
 * @param {string} str - target string
 * @returns {string} short name
 */
export const shortName = (str) => {
  const len = 20;
  if (str.length <= len) return str;
  return str.slice(0, len) + '...';
};
